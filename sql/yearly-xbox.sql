-- target dirty.csv
SELECT "Title",
    "Platform",
    "Status",
    "Rating",
    "Playtime"
FROM "HLTB"
WHERE (
        "Platform" in ("XSS", "X360", "Xbox")
        OR "Storefront" in ("EA Play", "Microsoft", "XGP")
    )
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
ORDER BY CASE
        WHEN "Playtime" IS NULL THEN 1
        ELSE 0
    END,
    LENGTH("Playtime") DESC,
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