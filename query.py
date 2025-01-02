#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import glob
import sqlite3
import sys
from datetime import datetime, timedelta


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


def query_csv(input_csv, output_csv, sql_query):
    # Read query from file
    with open(sql_query, "r", encoding="utf-8") as file:
        query = file.read()

    # Replace date on demand
    last_month_start, last_month_end = get_last_month_dates()
    query = query.replace("2024-09-01", last_month_start).replace(
        "2024-09-30", last_month_end
    )

    # Create a memory SQLite DB
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Read CSV and create table
    with open(input_csv, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        cursor.execute(f"CREATE TABLE HLTB ({', '.join(headers)})")
        cursor.executemany(
            # trunk-ignore(bandit/B608): intended SQL injection
            f"INSERT INTO HLTB VALUES ({', '.join(['?']*len(headers))})",
            reader,
        )

    cursor.execute(query)
    results = cursor.fetchall()

    with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([description[0] for description in cursor.description])
        writer.writerows(results)

    conn.close()


file_list = glob.glob("dirty.csv")

if len(file_list) > 0:
    # Read every matched file
    for filepath in file_list:
        NEW_FILE = "monthly.csv"
        query_csv(filepath, NEW_FILE, "sql/monthly.sql")
else:
    print("Sanitized CSV not found. Run `python hltb_sanitizer.py` first.")
    sys.exit()
