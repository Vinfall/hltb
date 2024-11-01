SELECT "Title",
    "Platform",
    "Storefront",
    "Status",
    "Rating",
    "Playtime"
FROM "HLTB"
WHERE "Finished" BETWEEN '2024-09-01' AND '2024-09-30' -- finished this month
    OR (
        "Finished" IS NULL
        AND NOT "Date" > '2024-09-30' -- Playing/Retired/Stalled
        AND NOT (
            "Date" < '2024-09-01' -- excluded earlier games
            AND NOT "Status" = 'Playing'
        )
    ) -- would get replaced in query.py
ORDER BY "Playtime" DESC;