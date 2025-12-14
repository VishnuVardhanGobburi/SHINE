CREATE TABLE shine_transformed.authors (
    author_id INT IDENTITY PRIMARY KEY,
    author_name NVARCHAR(200) UNIQUE NOT NULL
);


CREATE INDEX idx_authors_name
ON shine_transformed.authors(author_name);