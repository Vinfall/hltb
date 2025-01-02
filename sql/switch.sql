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
ORDER BY "Playtime" DESC,
    "Rating" DESC;