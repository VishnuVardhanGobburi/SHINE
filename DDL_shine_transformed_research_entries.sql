CREATE TABLE shine_transformed.research_entries (
    entry_id INT IDENTITY PRIMARY KEY,
    title NVARCHAR(300) NOT NULL,
    publication_year INT NULL,
    publication_type NVARCHAR(100),
    source NVARCHAR(200),
    annotation NVARCHAR(MAX) NOT NULL,
    methodology NVARCHAR(50),
    relevance_score TINYINT CHECK (relevance_score BETWEEN 1 AND 5),
    source_timestamp DATETIME,      -- propagated from RAW
    created_at DATETIME DEFAULT GETDATE()
);


CREATE INDEX idx_research_entries_year
ON shine_transformed.research_entries(publication_year);