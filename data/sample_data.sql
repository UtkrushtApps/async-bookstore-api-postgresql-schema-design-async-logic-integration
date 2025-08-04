-- Sample authors
INSERT INTO authors (name) VALUES ('J.K. Rowling'), ('George R.R. Martin'), ('Suzanne Collins'), ('Isaac Asimov'), ('J.R.R. Tolkien');
-- Sample categories
INSERT INTO categories (name) VALUES ('Fantasy'), ('Science Fiction'), ('Drama'), ('Adventure');
-- Sample books
INSERT INTO books (title, author_id, published_year) VALUES
('Harry Potter and the Sorcerer''s Stone', 1, 1997),
('A Game of Thrones', 2, 1996),
('The Hunger Games', 3, 2008),
('Foundation', 4, 1951),
('The Hobbit', 5, 1937);
-- Sample book_category
INSERT INTO book_category (book_id, category_id) VALUES
(1,1),(2,1),(3,3),(4,2),(5,1),(1,4),(2,4);
-- Insert 1000 more books for performance/concurrency testing
DO $$
DECLARE
i INT;
a INT;
c INT;
tx TEXT;
BEGIN
FOR i IN 6..1005 LOOP
  a := ((random()*4)::int + 1);
  tx := 'Book Title #' || i;
  INSERT INTO books (title, author_id, published_year) VALUES (tx, a, 1950 + (i%70));
  c := ((random()*3)::int + 1);
  INSERT INTO book_category (book_id, category_id) VALUES (i, c);
END LOOP;
END$$;