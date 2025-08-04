# FastAPI Async Bookstore – PostgreSQL Integration Task

## Task Overview
You are maintaining Utkrusht's online bookstore built on FastAPI. While routing and request/response validation are already in place, the project is suffering from slow search and listing endpoints due to missing database normalization, lack of async database queries, and absent indexes. Specifically, fetching books by author or by category times out as the dataset grows. You must refactor the PostgreSQL schema to define efficient relationships and indexes, and implement robust async database operations so all endpoints are performant and non-blocking. Integrate a simple async background task for logging book search operations.

## Guidance
- The current schema does not use foreign keys or proper normalization; some redundant fields exist.
- Blocking synchronous psycopg2 operations are used—replace with asyncpg for non-blocking access.
- Books, authors, and categories exist but lack normalized many-to-many and one-to-many modeling.
- Key data columns such as author_id and category_id are not indexed.
- The project already includes routing, pydantic schemas, CORS middleware, and error handling—your job is to fix the *database layer only*.
- Implement and test async DB interaction within the provided route/layout; do not modify route parameters or business logic signatures.
- Set up a background task that logs each book search (by author or category) to the database asynchronously.

## Database Access
- Host: <DROPLET_IP>
- Port: 5432
- Database: bookstore_db
- Username: bookstore_user
- Password: bookstore_pass
- Use any GUI/CLI tool (DBeaver, pgAdmin, psql) for schema, constraint, and query checks.

## Objectives
- Define normalized PostgreSQL tables (books, authors, categories, book_category) with correct relationships, primary/foreign keys, and indexes.
- Implement all async CRUD database functions using asyncpg—replace any blocking/sync code in database integration.
- Ensure search endpoints (GET /books?author=, GET /books?category=) are performant (limit response time per search to ≤ 250ms for 1000+ rows).
- Use FastAPI background tasks to log each book search to a separate logs table asynchronously.
- Guarantee that project passes all built-in endpoint tests and that async database access does not block the server.

## How to Verify
- Confirm all API endpoints (books, authors, categories) work with correct data and fast response times (test via /docs UI).
- Use EXPLAIN ANALYZE for search queries and verify indexes are used (no table scans on large book sets).
- Run the app under a simple concurrency tool (e.g., ApacheBench, autocannon) to verify non-blocking performance.
- Check the logs table to see recent book search logs inserted by the async background task.
