INSERT INTO shine_transformed.entry_keywords (entry_id, keyword_id)
SELECT DISTINCT
    t.entry_id,
    k.keyword_id
FROM shine_raw.research_entries_raw r
JOIN shine_transformed.research_entries t
    ON t.title = r.title
   AND t.source_timestamp = r.source_timestamp
CROSS APPLY STRING_SPLIT(r.keywords, ',') s
JOIN shine_transformed.keywords k
    ON k.keyword = LOWER(LTRIM(RTRIM(s.value)))
WHERE NOT EXISTS (
    SELECT 1
    FROM shine_transformed.entry_keywords ek
    WHERE ek.entry_id = t.entry_id
      AND ek.keyword_id = k.keyword_id
);