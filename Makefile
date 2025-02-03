# Dependencies & scripts
SANITIZER = hltb_sanitizer.py
BARCHART = hltb_barchartrace.py
PLOT = hltb_visualizer.py

# Default target, run one by one
all:
	$(MAKE) sanitize
	$(MAKE) plot

run: ## monthly workflow
	$(MAKE) sanitize
	$(MAKE) query
	$(MAKE) analyze

check: ## check invalid lines
	uv run debug.py

sanitize: clean check ## sanitize data
	uv run $(SANITIZER)
	uv run $(BARCHART)

query: sanitize ## generate monthly playlist
	@echo "Do not use python for this, period."

analyze: monthly.csv ## analyze monthly data
	uv run analyze.py

plot: sanitize ## generate plots
	uv run $(PLOT)

clean: ## clean outputs
	-rm clean.csv dirty.csv barchartrace-*.csv output/*.png output/word-frequency.txt
	-rm output/errors.csv

help: ## show this help
	@echo "Specify a command:"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help
