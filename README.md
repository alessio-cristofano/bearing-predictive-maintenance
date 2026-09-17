# IMS Bearing Predictive Maintenance Data Pipeline

![CI Status](https://github.com/alessio-cristofano/bearing-predictive-maintenance/actions/workflows/ci.yml/badge.svg)

## Overview
A modular, end-to-end data engineering pipeline designed to ingest, process, and extract features from high-frequency sensor data. Built using the IMS Bearing dataset (20 kHz sampling rate, 1-second snapshots), this project transitions raw, multi-gigabyte ASCII test-to-failure records into highly compressed, analytical Parquet tables ready for machine learning.

## Architecture & Tech Stack
* **Language & Layout:** Python 3.11+ using a strict `src/` package layout.
* **Orchestration:** Custom CLI built with `Click` for parameterized pipeline runs.
* **Compute & Storage:** `Polars` for high-speed columnar data processing; `DuckDB` for SQL-based analytical validation; `Parquet` with snappy compression for optimized I/O.
* **CI/CD & Quality:** Automated GitHub Actions pipeline enforcing `Ruff` (linting) and `Pytest` (unit testing) on every push.

## Pipeline Layers
1. **Bronze (Raw Ingestion):** Parses raw filename timestamps (YYYY.MM.DD.HH.MM.SS) and ingests thousands of individual ASCII files. Dynamically adapts to varying sensor configurations (e.g., 8-channel vs. 4-channel setups).
2. **Silver (Feature Extraction):** Aggregates raw vibration signals into statistical time-domain features (RMS, Kurtosis, Skewness, Peak-to-Peak) to reduce dimensionality while preserving failure signatures.

## Quickstart
```bash
# Clone and setup environment
git clone [https://github.com/alessio-cristofano/bearing-predictive-maintenance.git](https://github.com/alessio-cristofano/bearing-predictive-maintenance.git)
cd bearing-predictive-maintenance
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the pipeline for Dataset N (1,2 or 3)
python3 -m src.run_pipeline --dataset-id <N>