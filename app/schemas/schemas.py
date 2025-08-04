from pydantic import BaseModel
from typing import List, Optional

class BookCreate(BaseModel):
    title: str
    author: str
    categories: Optional[List[str]] = None
    published_year: int

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: int

class Author(BaseModel):
    id: int
    name: str

class Category(BaseModel):
    id: int
    name: str

class BookSearchLog(BaseModel):
    id: int
    action: str
    details: str
    created_at: str
