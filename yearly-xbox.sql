SELECT "Title",
    "Platform",
    "Storefront",
    "Status",
    "Rating",
    "Playtime"
FROM "HLTB"
WHERE "Storefront" in (
        "Xbox Game Pass",
        "Xbox Games w/ Gold",
        "Xbox Store",
        "Microsoft Store"
    ) -- tip: exclude all others for xgp as gold is down
    AND (
        "Finished" BETWEEN '2024-01-01' AND '2024-12-31' -- finished this year
        OR (
            "Finished" IS NULL
            AND NOT "Date" > '2024-12-31' -- Playing/Retired/Stalled
            AND NOT (
                "Date" < '2024-01-01' -- excluded earlier games
                AND NOT "Status" = 'Playing'
            )
        )
    )
ORDER BY "Playtime" DESC;