#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import glob

file_list = glob.glob("HLTB_Games_*.csv")

if len(file_list) > 0:
    # Read every matched file
    for filepath in file_list:
        new_file_name = filepath.replace("HLTB_Games_", "HLTB-sanitized-")
        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for i, line in enumerate(reader, start=1):
                # print invalid lines
                if len(line) != 32:
                    print(f"Line {i} has {len(line)} fields: {line}")
