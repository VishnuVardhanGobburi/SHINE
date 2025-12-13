INSERT INTO shine_transformed.keywords (keyword)
SELECT DISTINCT
    LOWER(LTRIM(RTRIM(value))) AS keyword
FROM shine_raw.research_entries_raw r
CROSS APPLY STRING_SPLIT(r.keywords, ',')
WHERE r.keywords IS NOT NULL
  AND LTRIM(RTRIM(value)) <> ''
  AND NOT EXISTS (
      SELECT 1
      FROM shine_transformed.keywords k
      WHERE k.keyword = LOWER(LTRIM(RTRIM(value)))
  );