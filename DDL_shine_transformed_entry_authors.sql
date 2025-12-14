CREATE TABLE shine_transformed.entry_authors (
    entry_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (entry_id, author_id),
    CONSTRAINT fk_entry_authors_entry
        FOREIGN KEY (entry_id)
        REFERENCES shine_transformed.research_entries(entry_id),
    CONSTRAINT fk_entry_authors_author
        FOREIGN KEY (author_id)
        REFERENCES shine_transformed.authors(author_id)
);