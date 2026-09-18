# Case Study: Phase 1 - Local Lakehouse Foundation

## The Challenge
The "Bearings Predictive Maintenance" dataset consists of high-frequency (20 kHz) IoT sensor telemetry capturing the run-to-failure lifecycle of mechanical bearings. The raw data was provided as thousands of headerless ASCII files containing exactly 20,480 floating-point measurements per 1-second snapshot (source: https://www.kaggle.com/datasets/vinayak123tyagi/bearing-dataset). 

My objective was to transition these raw, disjointed files into a structured, queryable data engineering pipeline capable of feeding downstream predictive maintenance models.

## Architectural Decisions & Trade-offs

### 1. Polars over Pandas for Ingestion
Processing over 20 million rows of ASCII text per dataset required high multithreading and memory efficiency. I selected `Polars` for the Bronze layer ingestion due to its Rust-backed columnar engine, which significantly outperformed standard `Pandas` performance.

### 2. Parquet as the Lakehouse Storage Format
Instead of loading the raw data into a traditional transactional database (like PostgreSQL), I serialized the ingested data into Parquet files. 
* **Impact:** Reduced multi-gigabyte raw ASCII folders into highly compressed, columnar files, optimizing local storage and setting the foundation for a future cloud migration to AWS S3.

### 3. DuckDB for Zero-Copy Analytics
To validate the Silver layer features (RMS, Kurtosis, Peak-to-Peak), I integrated `DuckDB`. This allowed me to execute analytical SQL queries directly against the local Parquet files without the overhead of spinning up a dedicated database server, demonstrating a modern "zero-copy" analytical workflow.

### 4. Strict Data Contracts
IoT sensor data is prone to packet loss and schema drift. I implemented defensive programming constraints in the ingestion layer:
* Validated exactly 20480 rows per snapshot.
* Dynamically mapped schemas based on varying sensor layouts (8 channels for Set 1 vs. 4 channels for Sets 2 and 3).
* Rejected null values to ensure downstream machine learning models receive continuous signal integrity.
However, it must be pointed out that none of these checks failed, as the dataset has a very high quality.
## Engineering Standards Applied
* **CI/CD Automation:** Configured GitHub Actions to run `pytest` suites and `Ruff` static code analysis on every push, ensuring the pipeline remains unbroken as features are added.
* **Modular Design:** Decoupled hardware constraints and dataset configurations into a `config.yaml` to separate business logic from Python execution.
* **CLI Orchestration:** Built a parameterized `Click` interface to dynamically execute pipelines across different datasets.

## Next Phase
Phase 2 will migrate this local architecture into an AWS Cloud Lakehouse.