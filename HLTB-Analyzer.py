#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt


def calculate_month_playtime(df):
    # Get the current date
    today = pd.to_datetime("today").normalize()  # noqa

    # Get the start and end dates of the month
    # month_start = (today - pd.offsets.MonthBegin(1)).strftime('%Y-%m-%d')
    # month_end = (today - pd.offsets.MonthEnd(1)).strftime('%Y-%m-%d')
    # pd.offsets does not work, so hardcode start and end
    month_start = "2023-11-01"
    month_end = "2023-11-30"

    # Convert columns to Timestamp
    df["Date"] = pd.to_datetime(df["Date"])
    df["Lastmod"] = pd.to_datetime(df["Lastmod"])

    # Filter rows for the month and games that occupy more than 15 days
    month_rows = df[
        (df["Lastmod"] >= month_start)
        & (df["Lastmod"] <= month_end)
        & (df["Lastmod"] - df["Date"] <= pd.Timedelta(days=15))
    ]

    # Convert playtime of month to time strings and sum them
    month_playtime = pd.to_timedelta(month_rows["Playtime"]).sum()

    # Convert month_playtime to the format HH:MM:SS
    total_seconds = month_playtime.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    month_playtime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return month_playtime_str


# Read CSV file
file_list = glob.glob("HLTB-sanitized-*.csv")
if len(file_list) > 0:
    filepath = file_list[0]
    df = pd.read_csv(filepath)
else:
    print("HLTB sanitized CSV not found.")
    exit()

# Analyze data
# Calculate the playtime of last month
month_playtime = calculate_month_playtime(df)
# Print the result
print("Monthly playtime:", month_playtime)

# Debug preview
# print(df)
