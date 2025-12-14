CREATE TABLE shine_raw.research_entries_raw (
    raw_id INT IDENTITY PRIMARY KEY,
    title NVARCHAR(300),
    authors NVARCHAR(500),                 
    publication_year NVARCHAR(10),          
    publication_type NVARCHAR(100),
    source NVARCHAR(200),
    keywords NVARCHAR(500),                 
    annotation NVARCHAR(MAX),
    methodology NVARCHAR(50),
    relevance_score NVARCHAR(10),
    source_timestamp DATETIME,              
    loaded_at DATETIME DEFAULT GETDATE()
);