#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np


def plot_storefront_for_pc_platform(df):
    # Select rows where Platform is PC and exclude Steam
    pc_storefront_counts = df[(df["Platform"] == "PC") & (df["Storefront"] != "Steam")][
        "Storefront"
    ].value_counts()

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(pc_storefront_counts, labels=pc_storefront_counts.index, autopct="%1.1f%%")
    ax.set_title(
        "Storefront Distribution for PC Platform (Excluding Steam) (Pie Chart)"
    )
    plt.show()


def plot_platform_distribution_exclude_pc(df):
    # Select rows where Platform is not PC
    platform_counts = df[df["Platform"] != "PC"]["Platform"].value_counts()

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(platform_counts, labels=platform_counts.index, autopct="%1.1f%%")
    ax.set_title("Platform Distribution (Excluding PC) (Pie Chart)")
    plt.show()


# Read CSV file
file_list = glob.glob("HLTB-sanitized-*.csv")
if len(file_list) > 0:
    filepath = file_list[0]
    df = pd.read_csv(filepath)
else:
    print("HLTB sanitized CSV not found.")
    exit()

# Generate and display charts
plot_storefront_for_pc_platform(df)
plot_platform_distribution_exclude_pc(df)

# Debug preview
# print(df)
