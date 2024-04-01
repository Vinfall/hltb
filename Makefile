# Commands
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

# Install dependencies for Python
install: $(REQUIREMENTS)
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
