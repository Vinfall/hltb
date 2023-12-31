#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import numpy as np
import pandas as pd


# Deal with caveats in exported CSV
def sanitized_dataframe(df):
    # Drop unused custom tag column index between "Blocked" and "Completed"
    blocked_index = df.columns.get_loc("Blocked")
    # completed_index = df.columns.get_loc("Completed")
    middle_column_index = blocked_index + 1
    df.drop(df.columns[middle_column_index], axis=1, inplace=True)

    # Rename second "Completed" column (the one before "Progress") to "Completed Date"
    progress_index = df.columns.get_loc("Progress")
    columns = df.columns.tolist()
    columns[progress_index - 1] = "Completed Date"
    df.columns = columns

    # Replace "--" (implying null time) with NaN
    df.replace("--", np.nan, inplace=True)

    # Exclude blocked games
    df = df[df["Blocked"] != "✓"]

    return df


def determine_status(row):
    if row["Playing"] == "✓":
        return "Playing"
    elif row["Backlog"] == "✓":
        return "Backlog"
    elif row["Replay"] == "✓":
        return "Replay"
    elif row["Stalled"] == "✓":
        return "Stalled"
    elif row["Completed"] == "✓":
        return "Completed"
    elif row["Retired"] == "✓":
        return "Retired"
    else:
        return ""


# Read CSV file
file_list = glob.glob("HLTB_Games_*.csv")
if len(file_list) > 0:
    filepath = file_list[0]
    df = pd.read_csv(filepath)
    new_file_name = filepath.replace("HLTB_Games_", "HLTB-sanitized-")
else:
    print("HLTB exported CSV not found.")
    exit()

df = sanitized_dataframe(df)

# Convert to time type
df[["Progress", "Main Story", "Main + Extras", "Completionist"]] = df[
    ["Progress", "Main Story", "Main + Extras", "Completionist"]
].apply(pd.to_timedelta, errors="coerce")
# Exclude NaN line
df = df.dropna(
    subset=["Progress", "Main Story", "Main + Extras", "Completionist"], how="all"
)
# Choose the maximum one
max_playtime = df[["Progress", "Main Story", "Main + Extras", "Completionist"]].max(
    axis=1
)
# Convert back to string as "Playtime"
max_playtime_hours = max_playtime.dt.total_seconds().div(3600)
df["Playtime"] = max_playtime_hours.apply(
    lambda x: "{:02d}:{:02d}:{:02d}".format(
        int(x // 1), int((x % 1) * 60), int((x * 60) % 60)
    )
)

# Use "Added" column as "Date"
df["Added"] = pd.to_datetime(df["Added"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
df["Date"] = df["Added"].dt.strftime("%Y-%m-%d")

# Choose nearest date between "Completed Date" & "Updated" as "Lastmod"
df["Completed Date"] = pd.to_datetime(
    df["Completed Date"], format="%Y-%m-%d", errors="coerce"
)
df["Updated"] = pd.to_datetime(
    df["Updated"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
)
df["Lastmod"] = df[["Completed Date", "Updated"]].max(axis=1).dt.strftime("%Y-%m-%d")

# Status
df["Status"] = df.apply(determine_status, axis=1)

# Rating, 10/10 not 100/100
df["Rating"] = df["Review"] // 10
# Replace "Not Rated" with NaN
df["Rating"] = df["Rating"].replace(0, np.nan)
# Convert to integer while keeping NaN
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").astype("Int64")

# Drop the "Review" column
df = df.drop("Review", axis=1)
# Rename the "Review Notes" column to "Review"
df = df.rename(columns={"Review Notes": "Review"})

# Keep only these columns
df = df[
    [
        "Title",
        "Platform",
        "Storefront",
        "Status",
        "Rating",
        "Date",
        "Lastmod",
        "Playtime",
        "Review",
    ]
]

# Debug preview
print(df)

# Export to CSV
df.to_csv(new_file_name, index=False, quoting=1)
