CREATE TABLE shine_transformed.entry_keywords (
    entry_id INT NOT NULL,
    keyword_id INT NOT NULL,
    PRIMARY KEY (entry_id, keyword_id),
    CONSTRAINT fk_entry_keywords_entry
        FOREIGN KEY (entry_id)
        REFERENCES shine_transformed.research_entries(entry_id),
    CONSTRAINT fk_entry_keywords_keyword
        FOREIGN KEY (keyword_id)
        REFERENCES shine_transformed.keywords(keyword_id)
);