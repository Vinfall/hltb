SELECT "Title",
    "Platform",
    "Storefront",
    "Status",
    "Rating",
    "Playtime"
FROM "HLTB"
WHERE "Platform" = "Nintendo Switch"
    OR (
        "Storefront" = "Nintendo eShop" -- Switch Arcade game
        AND "Platform" NOT in ("Nintendo 3DS", "Wii", "Wii U") -- eShop used to be a 3DS/Wii/WiiU thing
    )
ORDER BY "Playtime" DESC,
    "Rating" DESC;