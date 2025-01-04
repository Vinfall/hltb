-- target dirty.csv
SELECT "Title",
    "Platform",
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
ORDER BY LENGTH("Playtime") DESC,
    -- 100:00:00 > 99:59:59
    "Playtime" DESC,
    "Rating" DESC,
    CASE
        WHEN "Status" = "Completed" THEN 1
        WHEN "Status" = 'Playing' THEN 2
        WHEN "Status" = 'Stalled' THEN 3
        WHEN "Status" = 'Backlog' THEN 4
        WHEN "Status" = 'Retired' THEN 5
        ELSE 5 -- status rank
    END;