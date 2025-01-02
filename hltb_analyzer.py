#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib

import pandas as pd

# Import functions from query
query_module = importlib.import_module("query")

# Preferred finished date, accepted values: "Finished", "Lastmod"
DATE_COL = "Finished"


def month_playtime_rough(df):
    # TODO: move to query.py
    # Get the start and end dates of the month
    month_start, month_end = query_module.get_last_month_dates()

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

    # Format month_playtime to HH:MM:SS
    total_seconds = month_playtime.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    month_playtime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return month_playtime_str


def month_playtime_accurate(df):
    month_playtime = pd.to_timedelta(df["Playtime"]).sum()

    # Format month_playtime to HH:MM:SS
    total_seconds = month_playtime.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    month_playtime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return month_playtime_str


# Calculate the playtime of last month
def calc(filename):
    df = pd.read_csv(filename)
    # Debug preview
    # print(df.head())

    last_month_playtime = (
        month_playtime_rough(df)
        if filename == "clean.csv"
        else month_playtime_accurate(df)
    )

    print("Monthly playtime:", last_month_playtime)


calc("clean.csv")
calc("monthly.csv")
