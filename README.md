# HLTB Linear & Temporal Breakdown

## Intro

[HowLongToBeat](https://howlongtobeat.com) is a website that helps your track play times, which is also [in collaboration with Microsoft](https://news.xbox.com/en-us/2022/09/14/september-updates-xbox-app-on-pc/) to show approximate competition time for the Xbox app on PC. The best thing is you can export your records to a CSV file so you really own your data, instead of relying on a third party.

This is a linear and temporal data analysis & visualization based on the exported CSV using Python libraries, notably `numpy`, `pandas` and `matplotlib`, and only tested on GNU/Linux with Python 3.12.

## Install

```python
# Clone repo
git clone https://github.com/Vinfall/hltb
cd hltb
# Use venv if needed
virtualenv .venv
source ./.venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

Now you are good to go ahead.

## Usage

0. Export your HLTB data in options. Alternatively, you can use provided [`HLTB_Games_example.csv`](example/HLTB_Games_example.csv) in `example` folder for tests.

1. Run the scripts.

The following information may be useful to you:
- [`HLTB-Sanitizer.py`](HLTB-Sanitizer.py): sanitize exported data
  - Edit `BLOCK_TAGS` to exluded games with certain tags
  - Edit `CUSTOM_TAGS` to recognize your custom tab names
  - Change `SCORE_MAX` to `100` if you prefer Percentage System
- [`HLTB-Analyzer.py`](HLTB-Analyzer.py): analyze *sanitized* data
  - Adjust `MIN_TIMES` to change the word frequency limit
  - Adjust `DATE_COL` if you don't always add a completion date
- [`HLTB-Visualizer.py`](HLTB-Visualizer.py): generate a few ugly charts from *sanitized* data
  - Control plot behavior via `SHOW_PLOT`: patch CSV to meet the criteria of [batchartrace](https://github.com/FabDevGit/barchartrace)
- [`HLTB-Barchartrace.py`](HLTB-Barchartrace.py)
  - Adjust `DATE_COL` if you don't always add a completion date


That's it. You can find example charts and other information on [my blog](https://blog.vinfall.com/posts/2023/11/hltb/), or just read code comments.

## [License](LICENSE)

GLWTPL (Good Luck With That Public License)
