#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import csv
import glob

file_list = glob.glob("HLTB_Games_*.csv")

if len(file_list) > 0:
    # Read every matched file
    for filepath in file_list:
        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for i, line in enumerate(reader, start=1):
                # print invalid lines
                if len(line) != 33:
                    print(f"Line {i} has {len(line)} fields: {line}")
