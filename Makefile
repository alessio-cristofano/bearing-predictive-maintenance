.PHONY: setup lint test run clean

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

ID?=2

setup:
	@echo "Creating virtual environment and installing dependencies..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

lint:
	@echo "Running Ruff linter..."
	$(PYTHON) -m ruff check .

test:
	@echo "Running Pytest suite..."
	$(PYTHON) -m pytest tests/

run:
	@echo "Executing pipeline for Dataset $(ID)..."
	$(PYTHON) -m src.run_pipeline --dataset-id $(ID)

clean:
	@echo "Cleaning up caches and virtual environment..."
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +