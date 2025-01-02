#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import sys

import matplotlib.pyplot as plt
import pandas as pd
from imageio import imread  # noqa: F401
from wordcloud import WordCloud

# import numpy as np

# Show plot or save to file, True means show plot
SHOW_PLOT = {
    "storefront_for_pc_platform": False,
    "platform_distribution_exclude_pc": True,
    "review_wordcloud": False,
}


def plot_storefront_for_pc_platform(df, show_plot):
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
    if show_plot is True:
        # Show the plot
        plt.show()
    else:
        # Save the plot to file
        plt.savefig("output/pc-storefront.png")


def plot_platform_distribution_exclude_pc(df, show_plot):
    # Select rows where Platform is not PC
    platform_counts = df[df["Platform"] != "PC"]["Platform"].value_counts()

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(platform_counts, labels=platform_counts.index, autopct="%1.1f%%")
    ax.set_title("Platform Distribution (Excluding PC) (Pie Chart)")
    if show_plot is True:
        plt.show()
    else:
        plt.savefig("output/platform-distribution.png")


def generate_review_wordcloud(df, show_plot):
    # mask = imread("mask.png")
    # Define stop words
    # fmt: off
    stop_words = {'the', 'and', 'to', 'of', 'is', 'in', 'it', 'this', 'that',
        'was', 'as', 'for', 'with', 'on', 'at', 'by', 'from', 'are', 'you',
        'your', 'we', 'our', 'us', 'i', 'me', 'my', 'mine', 'he', 'him',
        'his', 'she', 'her', 'hers', 'they', 'them', 'their', 'theirs',
        'nan', 'its', 'also', 'im'}
    # fmt: on

    # Concatenate all the reviews into a single string
    text = " ".join(df["Review"].astype(str).tolist())

    # Create a WordCloud object
    w = WordCloud(
        width=800,
        height=400,
        background_color="white",
        # font_path="some-font.ttf",
        max_words=100,
        stopwords=stop_words,
        # mask=mask,
    )
    w.generate(text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(w, interpolation="bilinear")
    plt.axis("off")
    if show_plot is True:
        plt.show()
    else:
        plt.savefig("output/review-wordcloud.png")


file_list = glob.glob("clean.csv")
if len(file_list) > 0:
    # Read only the first file
    filepath = file_list[0]
    df_raw = pd.read_csv(filepath)
else:
    print("Sanitized CSV not found. Run `python hltb_sanitizer.py` first.")
    sys.exit()

# Generate and display charts
plot_storefront_for_pc_platform(df_raw, SHOW_PLOT["storefront_for_pc_platform"])
plot_platform_distribution_exclude_pc(
    df_raw, SHOW_PLOT["platform_distribution_exclude_pc"]
)
generate_review_wordcloud(df_raw, SHOW_PLOT["review_wordcloud"])
