INSERT INTO shine_transformed.research_entries (
    title,
    publication_year,
    publication_type,
    source,
    annotation,
    methodology,
    relevance_score,
    source_timestamp
)
SELECT
    r.title,
    TRY_CAST(r.publication_year AS INT),
    r.publication_type,
    r.source,
    r.annotation,
    r.methodology,
    TRY_CAST(r.relevance_score AS TINYINT),
    r.source_timestamp
FROM shine_raw.research_entries_raw r
WHERE NOT EXISTS (
    SELECT 1
    FROM shine_transformed.research_entries t
    WHERE t.title = r.title
      AND t.source_timestamp = r.source_timestamp
);
