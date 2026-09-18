# IMS Bearing Predictive Maintenance Data Pipeline

![CI Status](https://github.com/alessio-cristofano/bearing-predictive-maintenance/actions/workflows/ci.yml/badge.svg)

## Overview
A modular, end-to-end data engineering pipeline designed to ingest, process, and extract features from high-frequency sensor data. Built using the IMS Bearing dataset (20 kHz sampling rate, 1-second snapshots), this project transitions raw, multi-gigabyte ASCII test-to-failure records into highly compressed, analytical Parquet tables ready for machine learning.
## Portfolio Case Studies
Read the detailed technical breakdowns of my engineering decisions, architectural trade-offs, and pipeline performance:
* [Phase 1 Case Study: Building a Local Lakehouse for Bearings Predictive Maintenance](./docs/phase1_case_study.md)
* *Phase 2: Cloud Migration (In Progress)*

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
# Clone the repository
git clone [https://github.com/alessio-cristofano/bearing-predictive-maintenance.git](https://github.com/alessio-cristofano/bearing-predictive-maintenance.git)
cd bearing-predictive-maintenance

# Create the virtual environment and install dependencies
make setup

# Run the data quality tests
make test

# Execute the Medallion pipeline for the specified dataset_id (1,2 or 3). Default is 2.
make run ID=<dataset_id>