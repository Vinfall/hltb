#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import importlib

import pandas as pd

# Import functions from HLTB-Sanitizer
sanitizer_module = importlib.import_module("HLTB-Sanitizer")

# Tags to exclude from results, possible to use multiple tags, exmaple: ["Backlog", "Retired"]
BLOCK_TAGS = ["Blocked"]
# Custom tab names
CUSTOM_TAGS = ["Stalled"]
# Preferred finished date, accepted values: "Finished", "Lastmod"
DATE_COL = "Finished"
# Accepted vlaues: "Platform", "Storefront"
DIVISION = "Platform"


# Organize sanitized CSV
def sort_data(df):
    # Define the sort keys in the desired order
    sort_keys = ["Date", DATE_COL, "Platform", "Storefront", "Title"]

    # Sort the data based on the sort keys
    df_sorted = df.sort_values(by=sort_keys, na_position="last")

    # Reset the index of the sorted DataFrame
    df_sorted = df_sorted.reset_index(drop=True)

    # Return the sorted DataFrame
    return df_sorted[sort_keys]


def calculate_number(df, division):
    # Sort the DataFrame by 'Date' column in ascending order
    df_sorted = df.sort_values(by="Date")

    # Initialize an empty list to store the calculated 'Number' values
    number_values = []

    # Iterate over each row in the sorted DataFrame
    for _index, row in df_sorted.iterrows():
        # Get the current 'Date' and 'Platform'/'Storefront' values
        current_date = row["Date"]
        current_platform = row[division]

        # Count the occurrences of the current 'Platform'/'Storefront' in the rows with dates up to and including the current date
        count = (
            df_sorted.loc[df_sorted["Date"] <= current_date]
            .loc[df_sorted[division] == current_platform]
            .shape[0]
        )

        # Append the count to the list of 'Number' values
        number_values.append(count)

    # Add the 'Number' column to the DataFrame
    df_sorted["Number"] = number_values

    # Create a new DataFrame with only the 'Date', 'Platform'/'Storefront', and 'Number' columns
    df_sorted = df_sorted[[division, "Date", "Number"]]

    # Drop the duplicate rows
    df_sorted = df_sorted.drop_duplicates()

    # Filter out rows where 'Number' is 0
    df_sorted = df_sorted[df_sorted["Number"] != 0]

    # Filter out rows where 'Date' is later than '2022-10-31'
    # df_sorted = df_sorted[df_sorted['Date'] <= '2022-10-31']

    # Create a new DataFrame with all unique 'Date' and 'Platform'/'Storefront' combinations
    unique_dates = df_sorted["Date"].unique()
    unique_platforms = df_sorted[division].unique()
    new_index = pd.MultiIndex.from_product(
        [unique_dates, unique_platforms], names=["Date", division]
    )
    # new_df = df_sorted.set_index(['Date', division]).reindex(new_index)
    new_df = pd.DataFrame(index=new_index).reset_index()

    # Merge the new DataFrame with the sorted DataFrame
    merged_df = pd.merge(new_df, df_sorted, on=["Date", division], how="left")

    # Forward fill the missing values within each group of same division values
    merged_df["Number"] = merged_df.groupby(division)["Number"].ffill()

    # Fill the first 'Number' value of every division values with 0
    merged_df["Number"] = merged_df.groupby(division)["Number"].transform(
        lambda x: x.fillna(0)
    )

    return merged_df


def sanitized_dataframe_post(df, division):
    # Use shorter alias for platform/storefront
    if division == "Platform":
        df["Platform"] = df["Platform"].replace(
            {
                "NES": "FC",
                "Super Nintendo": "SFC",
                "Nintendo DS": "NDS",
                "Nintendo 3DS": "3DS",
                "Nintendo 64": "N64",
                "Nintendo GameCube": "NGC",
                "Nintendo Switch": "Switch",
                "Game Boy": "GB",
                "Game Boy Color": "GBC",
                "Game Boy Advance": "GBA",
                "Xbox 360": "X360",
                "Xbox Series X/S": "XSS",
                "PlayStation VR": "PSVR",
                "PlayStation Vita": "PSV",
                "PlayStation Portable": "PSP",
                "PlayStation 5": "PS5",
                "PlayStation 4": "PS4",
                "PlayStation 3": "PS3",
                "PlayStation 2": "PS2",
                "PlayStation 1": "PS1",
                "Sega Master System": "SMS",
                "Sega Mega Drive/Genesis": "MD",
                "Sega Saturn": "SS",
                "Sega Game Gear": "GG",
                "Neo Geo Pocket": "NGPC",
                "WonderSwan": "WSC",
                "NEC PC-98": "PC-98",
                "TurboGrafx-16": "PCE",
                "TurboGrafx-CD": "PCE-CD",
                "Oculus Quest": "Meta Quest",
            }
        )
    elif division == "Storefront":
        df["Storefront"] = df["Storefront"].replace(
            {
                "Direct Download": "DL",
                "Xbox Game Pass": "XGP",
                "Xbox Games w/ Gold": "XGP",
                "Xbox Store": "Xbox",
                "Microsoft Store": "Microsoft",
                "Ubisoft Connect": "Ubisoft",
                "Nintendo eShop": "eShop",
                "Google Play Pass": "Play Pass",
                "Epic Games": "EGS",
                "PlayStation Plus": "PS+",
                "PlayStation Store": "PSN",
                "itch.io": "itch",
            }
        )
    else:
        print("Invalid division. Exiting.")
        exit()

    return df


# File naming scheme
file_list = glob.glob("HLTB_Games_*.csv")
# Skip problematic lines
skip_rows = [4130]

# Read CSV file
if len(file_list) > 0:
    # Sanitize every file
    for filepath in file_list:
        new_file_name = filepath.replace(
            "HLTB_Games_", "HLTB-barchartrace-by-" + DIVISION.lower() + "-"
        )
        df = pd.read_csv(filepath, skiprows=skip_rows)
        df = sanitizer_module.sanitized_dataframe(df)
        df = sanitizer_module.date_sanitize(df)

        # Sort data
        df = sort_data(df)

        # Calculate number of platforms at a specific date
        df = calculate_number(df, DIVISION)

        # Post sanitization
        df = sanitized_dataframe_post(df, DIVISION)

        # Debug preview
        print(df.head())

        # Export to CSV
        df.to_csv(new_file_name, index=False, quoting=1)
        print("Now drop output to https://fabdevgit.github.io/barchartrace")
else:
    print("HLTB sanitized CSV not found.")
    exit()
