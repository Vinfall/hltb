SELECT *
FROM HLTB
WHERE "Platform" NOT IN (
        "Browser",
        "Nintendo Switch",
        "PC",
        "PlayStation 4",
        "Xbox Series X/S"
    ) -- exclude browser & recent generation
    AND "Storefront" NOT IN ("Google Play", "Google Play Pass") -- exclude mobile
ORDER BY "Lastmod" DESC,
    "Finished" DESC,
    "Date" DESC