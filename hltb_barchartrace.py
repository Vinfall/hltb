#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import importlib
import sys

import pandas as pd

# Import functions from hltb_sanitizer
sanitizer_module = importlib.import_module("hltb_sanitizer")

# Custom tab names
CUSTOM_TAGS = ["Stalled"]
# Tags to exclude from results
# Tip: possible to use multiple tags, exmaple: ["Backlog", "Retired"]
BLOCK_TAGS = ["Ignored"]
# Same as above, but for divisions (i.e. platforms/storefront)
# Tip: useful if certain platforms extremely exceed others
BLOCK_DIVS = ["PC", "Browser"]
# Preferred finished date, accepted values: "Finished", "Lastmod"
DATE_COL = "Finished"
# Accepted vlaues: "Platform", "Storefront"
# Tip: this should be in sync with BLOCK_DIVS
DIVISION = "Platform"
# ISO Date range
DATE_RANGE = True
DATE_START = "2024-01-01"
DATE_END = "2024-12-31"


# Organize sanitized CSV
def sort_data(df):
    # Filter data range
    if DATE_RANGE:
        df = df[(df["Date"] >= DATE_START) & (df["Date"] <= DATE_END)]

    # Exclude games on excluded platforms
    for block_div in BLOCK_DIVS:
        df = df[df[DIVISION] != block_div]

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

        # Count occurrences of current 'Platform'/'Storefront' in the rows with dates to date
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


# File naming scheme
file_list = glob.glob("HLTB_Games_*.csv")
# Skip problematic lines
skip_rows = []

# Read CSV file
if len(file_list) > 0:
    # Sanitize every file
    for filepath in file_list:
        NEW_FILE = "barchartrace-by-" + DIVISION.lower() + ".csv"
        df_raw = pd.read_csv(filepath, skiprows=skip_rows)
        df_mod = sanitizer_module.sanitized_dataframe(df_raw)
        df_mod = sanitizer_module.date_sanitize(df_mod)

        # Sort data
        df_mod = sort_data(df_mod)

        # Calculate number of platforms at a specific date
        df_mod = calculate_number(df_mod, DIVISION)

        # Post sanitization
        df_mod = sanitizer_module.minify_platform(df_mod, DIVISION)

        # Debug preview
        # print(df_mod.head())

        # Export to CSV
        df_mod.to_csv(NEW_FILE, index=False, quoting=1)
        print("Now drop output to https://fabdevgit.github.io/barchartrace")
else:
    print("HLTB sanitized CSV not found. Run `python hltb_sanitizer.py` first.")
    sys.exit()
