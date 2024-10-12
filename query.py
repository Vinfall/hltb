#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import sqlite3
import sys

import pandas as pd


def query_csv(input_csv, output_csv, sql_query):
    # Read query from file
    with open(sql_query, "r", encoding="utf-8") as file:
        query = file.read()

    # Create a memory SQLite DB
    DB_CONN = sqlite3.connect(":memory:")
    df = pd.read_csv(input_csv)
    df.to_sql("HLTB", DB_CONN, index=False, if_exists="replace")

    result_df = pd.read_sql_query(query, DB_CONN)
    result_df.to_csv(output_csv, index=False)

    DB_CONN.close()


file_list = glob.glob("HLTB-sanitized-*.csv")

if len(file_list) > 0:
    # Read every matched file
    for filepath in file_list:
        new_file_name = filepath.replace("HLTB-sanitized-", "query-")
        query_csv(filepath, new_file_name, "monthly.sql")
else:
    print("Sanitized CSV not found. Run `python hltb_sanitizer.py` first.")
    sys.exit()
