# HLTB Linear & Temporal Breakdown

## Intro

[HowLongToBeat](https://howlongtobeat.com) is a website that helps your track play times, which is also [in collaboration with Microsoft](https://news.xbox.com/en-us/2022/09/14/september-updates-xbox-app-on-pc/) to show approximate competition time for the Xbox app on PC. The best thing is you can export your records to a CSV file so you really own your data, instead of relying on some unsecure third party.

This is a linear and temporal data analysis & visualization based on the exported CSV using Python libraries, notably numpy, pandas and matplotlib.

## Install

```python
# Clone repo
git clone https://github.com/Vinfall/hltb
cd hltb
# Use venv if needed
virtualenv venv
source ./venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

Now you are good to go ahead.

## Usage

0. Export your HLTB data in options. Alternatively, you can use provided `HLTB_Games_example.csv` in `example` folder for tests.

1. Choose the right script for you:

| Script | Function |
|---|---|
| `HLTB-Sanitizer.py` | Sanitize exported data |
| `HLTB-Visualizer.py` | Generate a few ugly charts |
| `HLTB-Barchartrace.py` | Patch CSV to meet the criteria of [batchartrace](https://github.com/FabDevGit/barchartrace) |

That's it. You can find example charts and other information on [my blog](https://blog.vinfall.com/posts/2023/11/hltb/), or just read code comments.

## License

GLWTPL (Good Luck With That Public License)
