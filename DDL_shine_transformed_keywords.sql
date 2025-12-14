CREATE TABLE shine_transformed.keywords (
    keyword_id INT IDENTITY PRIMARY KEY,
    keyword NVARCHAR(100) UNIQUE NOT NULL
);


CREATE INDEX idx_keywords_keyword
ON shine_transformed.keywords(keyword);