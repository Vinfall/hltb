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
ANALYZER = hltb_analyzer.py
PLOT = hltb_visualizer.py

# Default target, run one by one
all:
	$(MAKE) check
	$(MAKE) install
	$(MAKE) sanitize
	$(MAKE) analyze plot

# make run
run:
	$(MAKE) check
	$(MAKE) clean
	$(MAKE) sanitize
	$(MAKE) analyze
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

sanitize: $(SANITIZER) ## sanitize data
	$(PYTHON) $(SANITIZER)
	$(PYTHON) $(BARCHART)

analyze: $(ANALYZER) ## analyze data
	$(PYTHON) $(ANALYZER)

query: ## generate monthly playlist
	$(PYTHON) query.py

plot: $(PLOT) ## generate plots
	$(PYTHON) $(PLOT)

clean: ## clean up outputs
	-rm HLTB-sanitized-*.csv HLTB-barchartrace-*.csv query-*.csv output/*.png output/word-frequency.txt
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
