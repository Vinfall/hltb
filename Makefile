# Varables
VENV = .venv
# PYTHON = $(VENV)/bin/python
# PIP = $(VENV)/bin/pip
PYTHON = python
PIP = pip

# Dependencies & scripts
REQUIREMENTS = requirements.txt
SANITIZER = hltb_sanitizer.py
BARCHART = hltb_barchartrace.py
PLOT = hltb_visualizer.py

# Default target, run one by one
all:
	$(MAKE) install
	$(MAKE) sanitize
	$(MAKE) plot

run: ## run without venv
	$(MAKE) sanitize
	$(MAKE) plot

check: ## check invalid lines
	$(PYTHON) debug.py

install: $(VENV) ## install dependencies in venv
	$(PIP) install -r $(REQUIREMENTS)

$(VENV):
	@echo "Setting up virtualenv..."
	virtualenv $(VENV)
	source $(VENV)/bin/activate; \
	$(PIP) install -r $(REQUIREMENTS)

sanitize: clean check ## sanitize data
	$(PYTHON) $(SANITIZER)
	$(PYTHON) $(BARCHART)

query: sanitize ## generate monthly playlist
	$(PYTHON) query.py

analyze: query ## analyze monthly data
	$(PYTHON) analyze.py

plot: sanitize ## generate plots
	$(PYTHON) $(PLOT)

clean: ## clean outputs
	-rm clean.csv dirty.csv barchartrace-*.csv monthly.csv output/*.png output/word-frequency.txt
	-rm output/errors.csv

uninstall: ## uninstall venv & clean cache
	@echo "Cleaning up..."
	@deactivate || true
	rm -rf $(VENV)
	pip cache purge || true

help: ## show this help
	@echo "Specify a command:"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help
