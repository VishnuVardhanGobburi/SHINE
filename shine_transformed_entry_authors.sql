INSERT INTO shine_transformed.entry_authors (entry_id, author_id)
SELECT DISTINCT
    t.entry_id,
    a.author_id
FROM shine_raw.research_entries_raw r
JOIN shine_transformed.research_entries t
    ON t.title = r.title
   AND t.source_timestamp = r.source_timestamp
CROSS APPLY STRING_SPLIT(r.authors, ';') s
JOIN shine_transformed.authors a
    ON a.author_name = LTRIM(RTRIM(s.value))
WHERE NOT EXISTS (
    SELECT 1
    FROM shine_transformed.entry_authors ea
    WHERE ea.entry_id = t.entry_id
      AND ea.author_id = a.author_id
);