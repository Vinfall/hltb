# Varables
VENV = .venv
# PYTHON = $(VENV)/bin/python
# PIP = $(VENV)/bin/pip
PYTHON = python
PIP = pip

# Dependencies & scripts
REQUIREMENTS = requirements.txt
SANITIZER = HLTB-Sanitizer.py
BARCHART = HLTB-Barchartrace.py
ANALYZER = HLTB-Analyzer.py
PLOT = HLTB-Visualizer.py

# Default target, run one by one
all:
	$(MAKE) install
	$(MAKE) sanitize
	$(MAKE) analyze plot

# make run
run:
	$(MAKE) sanitize
	$(MAKE) analyze
	$(MAKE) plot

# Install dependencies for Python
install: $(VENV)
	$(PIP) install -r $(REQUIREMENTS)

$(VENV):
	@echo "Setting up virtualenv..."
	virtualenv $(VENV)
	source $(VENV)/bin/activate; \
	$(PIP) install -r $(REQUIREMENTS)

# Sanitize data
sanitize: $(SANITIZER)
	$(PYTHON) $(SANITIZER)
	$(PYTHON) $(BARCHART)

# Analyze data
analyze: $(ANALYZER)
	$(PYTHON) $(ANALYZER)

# Generate plots
plot: $(PLOT)
	$(PYTHON) $(PLOT)

# Clean up outputs
clean:
	-rm HLTB-sanitized-*.csv HLTB-barchartrace-*.csv output/*.png output/word-frequency.txt
	-rm output/errors.csv

# Uninstall and purge cache
uninstall:
	@echo "Cleaning up..."
	@deactivate || true
	rm -rf $(VENV)
	pip cache purge || true
