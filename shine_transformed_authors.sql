INSERT INTO shine_transformed.authors (author_name)
SELECT DISTINCT
    LTRIM(RTRIM(value)) AS author_name
FROM shine_raw.research_entries_raw r
CROSS APPLY STRING_SPLIT(r.authors, ';')
WHERE r.authors IS NOT NULL
  AND LTRIM(RTRIM(value)) <> ''
  AND NOT EXISTS (
      SELECT 1
      FROM shine_transformed.authors a
      WHERE a.author_name = LTRIM(RTRIM(value))
  );