#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import importlib
import re
import sys
from collections import Counter

import pandas as pd

# Import functions from query
query_module = importlib.import_module("query")

# Minimum threshold of words to show in word frequency analysis
MIN_TIMES = 10
# Preferred finished date, accepted values: "Finished", "Lastmod"
DATE_COL = "Finished"


def calculate_month_playtime(df):
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


def calculate_word_frequency(df, min_times):
    # Extract the "Review" column and convert to lowercase
    reviews = df["Review"].astype(str).str.lower()

    # Remove punctuation using regular expressions
    reviews = reviews.apply(lambda x: re.sub(r"[^\w\s]", "", x))

    # Define stop words
    # fmt: off
    stop_words = {'the', 'and', 'to', 'of', 'is', 'in', 'it', 'this', 'that',
        'was', 'as', 'for', 'with', 'on', 'at', 'by', 'from', 'are', 'you',
        'your', 'we', 'our', 'us', 'i', 'me', 'my', 'mine', 'he', 'him',
        'his', 'she', 'her', 'hers', 'they', 'them', 'their', 'theirs',
        'nan', 'its', 'also', 'im'}
    # fmt: on

    # Tokenize the reviews
    reviews = reviews.str.split()

    # Remove stop words
    reviews = reviews.apply(lambda x: [word for word in x if word not in stop_words])

    # Flatten the list of words
    words = [word for review in reviews for word in review]

    # Perform word frequency analysis
    word_counts = Counter(words)

    # Keep only words with count >= min_times
    word_counts = {
        word: count for word, count in word_counts.items() if count > min_times
    }

    # Sort words by frequency in descending order
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Save word frequencies to file
    with open("output/word-frequency.txt", "w", encoding="utf-8") as file:
        file.write("Word frequency analysis:\n")
        for word, count in sorted_word_counts:
            file.write(f"{word} {count}\n")
    print("Check output/word-frequency.txt for the results.")


# Read CSV file
file_list = glob.glob("HLTB-sanitized-*.csv")
if len(file_list) > 0:
    # Only use the first file
    filepath = file_list[0]
    df_raw = pd.read_csv(filepath)
else:
    print("Sanitized CSV not found. Run `python hltb_sanitizer.py` first.")
    sys.exit()

# Analyze data
# Calculate the playtime of last month
last_month_playtime = calculate_month_playtime(df_raw)
# Print the result
print("Monthly playtime:", last_month_playtime)
# Calculate word frequency in reviews
calculate_word_frequency(df_raw, MIN_TIMES)

# Debug preview
# print(df.head())
