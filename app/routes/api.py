from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Query
from app.schemas.schemas import Book, BookCreate, Author, Category, BookSearchLog
from app.database import db
from typing import List, Optional

router = APIRouter()

# Dependency to access DB connection
async def get_pool():
    if db.pool is None:
        await db.connect()
    return db.pool

# Simulate logging with async background task
def log_search(query: str, pool):
    async def _log():
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO logs (action, details, created_at)
                VALUES ($1, $2, NOW())
            """, "search", query)
    return _log

@router.get("/books", response_model=List[Book])
async def list_books(
    author: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    background_tasks: BackgroundTasks = None,
    pool=Depends(get_pool),
):
    q = "SELECT b.id, b.title, a.name as author, b.published_year FROM books b JOIN authors a ON b.author_id=a.id"
    conditions = []
    params = []
    if author:
        conditions.append("a.name = $1")
        params.append(author)
    if category:
        q += " JOIN book_category bc ON bc.book_id=b.id JOIN categories c ON c.id=bc.category_id"
        conditions.append(f"c.name = ${len(params)+1}")
        params.append(category)
    if conditions:
        q += " WHERE " + " AND ".join(conditions)
    q += " LIMIT 30"
    async with pool.acquire() as conn:
        records = await conn.fetch(q, *params)
    if background_tasks:
        query_str = f"author={author}, category={category}"
        background_tasks.add_task(log_search(query_str, pool))
    return [Book(id=r['id'], title=r['title'], author=r['author'], published_year=r['published_year']) for r in records]

@router.post("/books", response_model=Book)
async def create_book(book: BookCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        author_id = await conn.fetchval("SELECT id FROM authors WHERE name=$1", book.author)
        if not author_id:
            author_id = await conn.fetchval("INSERT INTO authors (name) VALUES ($1) RETURNING id", book.author)
        # Assign categories
        book_id = await conn.fetchval("""
            INSERT INTO books (title, author_id, published_year)
            VALUES ($1, $2, $3)
            RETURNING id
        """, book.title, author_id, book.published_year)
        if book.categories:
            for cat in book.categories:
                cat_id = await conn.fetchval("SELECT id FROM categories WHERE name=$1", cat)
                if not cat_id:
                    cat_id = await conn.fetchval("INSERT INTO categories (name) VALUES ($1) RETURNING id", cat)
                await conn.execute("INSERT INTO book_category (book_id, category_id) VALUES ($1, $2)", book_id, cat_id)
        rec = await conn.fetchrow("""
            SELECT b.id, b.title, a.name as author, b.published_year
            FROM books b JOIN authors a ON b.author_id=a.id WHERE b.id=$1
        """, book_id)
        return Book(id=rec['id'], title=rec['title'], author=rec['author'], published_year=rec['published_year'])

@router.get("/authors", response_model=List[Author])
async def list_authors(pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM authors ORDER BY name")
    return [Author(id=r['id'], name=r['name']) for r in rows]

@router.get("/categories", response_model=List[Category])
async def list_categories(pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM categories ORDER BY name")
    return [Category(id=r['id'], name=r['name']) for r in rows]

@router.get("/logs", response_model=List[BookSearchLog])
async def get_logs(pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, action, details, created_at FROM logs ORDER BY created_at DESC LIMIT 30")
    return [BookSearchLog(id=r['id'], action=r['action'], details=r['details'], created_at=r['created_at'].isoformat()) for r in rows]
