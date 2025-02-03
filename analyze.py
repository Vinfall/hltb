#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2.3"]
# ///

from datetime import datetime, timedelta

import pandas as pd

# Preferred finished date, accepted values: "Finished", "Lastmod"
DATE_COL = "Finished"


def get_last_month_dates():
    today = datetime.today()

    first_day_of_month = today.replace(day=1)
    last_month_end = first_day_of_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # month_start = "2024-12-01"
    # month_end = "2024-12-31"
    month_start, month_end = last_month_start.strftime(
        "%Y-%m-%d"
    ), last_month_end.strftime("%Y-%m-%d")
    print(month_start, month_end)

    return month_start, month_end


def playtime(filename):
    df = pd.read_csv(filename)
    # Debug preview
    # print(df.head())

    # Rough estimation
    if filename == "clean.csv":
        # Get the start and end dates of the month
        month_start, month_end = get_last_month_dates()

        # Convert columns to Timestamp
        df["Date"] = pd.to_datetime(df["Date"])
        df[DATE_COL] = pd.to_datetime(df[DATE_COL])

        # Filter rows for the month and games that occupy more than 15 days
        month_rows = df[
            (df[DATE_COL] >= month_start)
            & (df[DATE_COL] <= month_end)
            & (df[DATE_COL] - df["Date"] <= pd.Timedelta(days=15))
        ]

        # Convert playtime of month to time strings and sum them
        month_playtime = pd.to_timedelta(month_rows["Playtime"]).sum()
    # Accurate calculation
    else:
        month_playtime = pd.to_timedelta(df["Playtime"]).sum()

    # Format month_playtime to HH:MM:SS
    total_seconds = month_playtime.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    month_playtime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    print(month_playtime_str)


def rating(filename):
    df = pd.read_csv(filename)
    df.dropna(subset=["Rating"], inplace=True)

    # Debug preview
    # print(df)

    # Rated titles
    m = len(df)
    # Average rating, did not consider 100/100 scale rating
    n = round(df["Rating"].mean(), 3)
    # SD, same result as VAR.P in Excel
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.std.html
    sd = round(df["Rating"].var(ddof=0), 3)

    print(f"∑={m}, μ={n}/10, σ²={sd}")


playtime("clean.csv")
playtime("monthly.csv")
rating("monthly.csv")
