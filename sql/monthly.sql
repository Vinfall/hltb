SELECT "Title",
    CASE
        WHEN "Storefront" = 'itch.io' THEN "itch" -- prioritize itch
        WHEN "Platform" = 'PC' THEN "Storefront" -- PC stores
        ELSE "Platform" -- could be wrong, e.g. emulator as remaster
    END AS "Platform",
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
ORDER BY "Playtime" DESC,
    "Rating" DESC;