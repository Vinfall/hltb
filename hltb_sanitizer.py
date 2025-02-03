#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pandas>=2.2.3",
#   "numpy>=2.2.2"
# ]
# ///

import csv
import glob
import sys

import numpy as np
import pandas as pd

# Tags to exclude from results, possible to use multiple tags, exmaple: ["Backlog", "Retired"]
BLOCK_TAGS = ["Ignored"]
# Custom tab names
CUSTOM_TAGS = ["Stalled"]
# Rating scale, accepted values: 10, 100
SCORE_MAX = 10
# Keep entries with null time
KEEP_NA_TIME = True


# Deal with caveats in exported CSV
def sanitized_dataframe(df):
    # Find custom tag column index
    start_index = df.columns.get_loc("Replay")
    end_index = df.columns.get_loc("Completed")
    for column_index in range(start_index + 1, end_index):
        # Drop unused custom tag between "Replay" and "Completed"
        if (
            "Custom-1" in df.columns[column_index]
            or "Custom-2" in df.columns[column_index]
            or "Custom-3" in df.columns[column_index]
        ):
            df.drop(df.columns[column_index], axis=1, inplace=True)

    # Fix pandas FutureWarning
    pd.set_option("future.no_silent_downcasting", True)
    # Replace "--" (implying null time) with NaN
    df = df.replace("--", np.nan).infer_objects(copy=False)

    # Exclude games with unwanted tags
    for block_tag in BLOCK_TAGS:
        df = df[df[block_tag] != "X"]

    return df


def date_sanitize(df):
    # df = sanitized_df.copy()

    # Prefer "Start Date" over "Added" column as "Date"
    df["Added"] = pd.to_datetime(
        df["Added"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
    )
    df["Started"] = pd.to_datetime(df["Start Date"], format="%Y-%m-%d", errors="coerce")
    df["Date"] = df["Started"].combine_first(df["Added"]).dt.strftime("%Y-%m-%d")

    # Choose nearest date between "Completion Date" & "Updated" as "Lastmod"
    df["Finished"] = pd.to_datetime(
        df["Completion Date"], format="%Y-%m-%d", errors="coerce"
    )
    df["Updated"] = pd.to_datetime(
        df["Updated"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
    )
    df["Lastmod"] = df[["Finished", "Updated"]].max(axis=1).dt.strftime("%Y-%m-%d")
    return df


def determine_status(row):
    status_col = ["Playing", "Backlog", "Replay", "Completed", "Retired"]
    keys = status_col + CUSTOM_TAGS
    key = "; ".join([key for key in keys if row.get(key) == "X"])
    # Prioritize Replay status
    if "Replay" in key:
        key = "Replay"
    return key


def post_sanitize(sanitized_df):
    # Copy dataframe to remove pandas warnings
    df = sanitized_df.copy()
    # Allow robust change
    time_col = [
        "Progress",
        "Main Story",
        "Main + Extras",
        "Completionist",
        "Speed Any%",
        "Speed 100%",
    ]
    # Convert to time type
    df[time_col] = df[time_col].apply(pd.to_timedelta, errors="coerce")
    # Exclude NaN line
    if not KEEP_NA_TIME:
        df = df.dropna(subset=time_col, how="all")
    # Choose the largest one in time_col
    max_playtime = df[time_col].max(axis=1)
    # Convert back to string as "Playtime"
    df["Playtime"] = max_playtime.apply(
        lambda x: (
            "00:00:00"
            if pd.isna(x)
            else "{:02}:{:02}:{:02}".format(
                int(x.total_seconds() // 3600),
                int((x.total_seconds() % 3600) // 60),
                int(x.total_seconds() % 60),
            )
        )
    )

    # Date
    df = date_sanitize(df)
    # Status
    df["Status"] = df.apply(determine_status, axis=1)

    # Rating
    if SCORE_MAX == 10:
        df["Rating"] = df["Review"] // 10
    elif SCORE_MAX == 100:
        df["Rating"] = df["Review"]
    else:
        print("Invalid SCORE_MAX value.")
        sys.exit()
    # Replace "Not Rated" with NaN
    df["Rating"] = df["Rating"].replace(0, np.nan)
    # Convert to integer while keeping NaN
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").astype("Int64")
    # Drop the "Review" column
    df = df.drop("Review", axis=1)

    # Choose longest one among various notes as "Review"
    note_col = [
        "Review Notes",
        "General Notes",
        "Retired Notes",
        "Speed Any% Notes",
        "Speed 100% Notes",
    ]
    df["Review"] = df.apply(
        lambda row: max(
            (str(row[col]) if pd.notnull(row[col]) else "" for col in note_col),
            key=len,
        ),
        axis=1,
    )

    # Keep only these columns
    df = df[
        [
            "Title",
            "Platform",
            "Storefront",
            "Status",
            "Rating",
            "Date",
            "Finished",
            "Lastmod",
            "Playtime",
            "Review",
        ]
    ]

    return df


def minify_platform(df, division):
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
                "Wii U": "WiiU",
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
                "PlayStation": "PSX",
                "Sega Master System": "SMS",
                "Sega Mega Drive/Genesis": "MD",
                "Sega CD": "Mega-CD",
                "Sega Saturn": "SS",
                "Sega Game Gear": "GG",
                "Dreamcast": "DC",
                "Neo Geo Pocket": "NGPC",
                "Neo Geo": "NeoGeo",
                "WonderSwan": "WSC",
                "NEC PC-98": "PC-98",
                "TurboGrafx-16": "PCE",
                "TurboGrafx-CD": "PCE-CD",
                "Oculus Quest": "Meta Quest",
                "FM Towns": "Towns",
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
                "Epic Games": "Epic",
                "PlayStation Plus": "PS+",
                "PlayStation Store": "PSN",
                "itch.io": "itch",
            }
        )
    else:
        print("Invalid division. Exiting.")
        sys.exit()

    return df


def dirty_clean(df):
    df = df.drop(["Review"], axis=1)
    # Use shorter alias
    minify_platform(df, "Platform")
    minify_platform(df, "Storefront")

    # Merge storefront into platform
    # could be wrong, e.g. emulator as remaster

    cons = ["itch", "Play Pass", "EA Play", "Ubisoft+", "XGP"]
    conditions = [
        df["Storefront"].isin(cons),
        df["Platform"] == "PC",
        df["Platform"] == "Mobile",
    ]
    choices = [df["Storefront"]] * len(conditions)
    # Use np.select to apply the conditions and choices
    df["Platform"] = np.select(conditions, choices, default=df["Platform"])

    return df


# Read CSV file
file_list = glob.glob("HLTB_Games_*.csv")
# Catch/Skip problematic lines
error_list = []
skip_rows = []

if len(file_list) > 1:
    print("Multiple CSVs no longer supported.")
    sys.exit()
elif len(file_list) == 1:
    # for filepath in file_list:
    filepath = file_list[0]
    try:
        df_raw = pd.read_csv(filepath, skiprows=skip_rows)
        df_mod = sanitized_dataframe(df_raw)
        df_mod = post_sanitize(df_mod)

        # Debug preview
        # print(df_mod.head())

        # Export to CSV
        df_mod.to_csv("clean.csv", index=False, quoting=1)

        df_mod = dirty_clean(df_mod)
        df_mod.to_csv("dirty.csv", index=False, quoting=1)

    except pd.errors.ParserError as e:
        error_list.append((filepath, str(e)))
else:
    print("HLTB exported CSV not found. Please export from options page first.")
    sys.exit()

# Only create error file if there are errors
if error_list:
    with open("output/errors.csv", "w", newline="", encoding="utf-8") as error_f:
        error_writer = csv.writer(error_f)
        error_writer.writerow(["Filepath", "Error"])
        error_writer.writerows(error_list)
