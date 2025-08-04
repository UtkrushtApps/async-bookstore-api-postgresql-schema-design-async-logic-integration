-- NORMALIZED BOOKSTORE SCHEMA
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id),
    published_year INTEGER
);
CREATE TABLE book_category (
    book_id INTEGER NOT NULL REFERENCES books(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    PRIMARY KEY (book_id, category_id)
);
CREATE INDEX idx_books_author_id ON books(author_id);
CREATE INDEX idx_book_category_category_id ON book_category(category_id);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMP NOT NULL
);