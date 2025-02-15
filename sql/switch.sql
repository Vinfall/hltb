-- target dirty.csv
SELECT "Title",
    "Platform",
    "Storefront",
    "Status",
    "Rating",
    "Playtime"
FROM "HLTB"
WHERE "Platform" = "Switch"
    OR (
        "Storefront" = "eShop" -- Switch Arcade game
        AND "Platform" NOT in ("3DS", "Wii", "WiiU") -- eShop used to be a 3DS/Wii/WiiU thing
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