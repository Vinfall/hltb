SELECT "Title", "Platform", "Storefront", "Status", "Rating", "Playtime"
FROM "HLTB"
WHERE "Lastmod" BETWEEN '2024-09-01' AND '2024-09-30'
    AND ("Finished" IS NULL OR "Finished" BETWEEN '2024-09-01' AND '2024-09-30') -- would get replaced in query.py
ORDER BY "Playtime" DESC;