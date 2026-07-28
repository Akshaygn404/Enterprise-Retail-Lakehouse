# Enterprise Retail Lakehouse

An end-to-end Data Engineering project that demonstrates the design and implementation of a modern Lakehouse architecture using PySpark, Delta Lake, Apache Airflow, PostgreSQL, and Power BI.

The project processes retail sales data through a Medallion Architecture (Bronze → Silver → Gold), automates the ETL pipeline using Apache Airflow, stores analytics-ready data in PostgreSQL, and visualizes business insights using Power BI.

---

## Architecture

```
                        Raw Retail CSV Files
                                │
                                ▼
                    Bronze Layer (Delta Lake)
                 Raw Data Ingestion + Metadata
                                │
                                ▼
                   Silver Layer (Delta Lake)
             Data Cleaning & Business Transformations
                                │
                                ▼
                    Gold Layer (Delta Lake)
             Star Schema (Dimensions + Fact Table)
                                │
                                ▼
                 PostgreSQL Data Warehouse
                                │
                                ▼
                      Power BI Dashboard
                                │
                                ▼
                    Business Insights & Analytics
```

The entire pipeline is orchestrated using **Apache Airflow**.

---

# Tech Stack

| Category | Technologies |
|-----------|-------------|
| Programming | Python |
| Data Processing | PySpark |
| Storage | Delta Lake |
| Workflow Orchestration | Apache Airflow |
| Data Warehouse | PostgreSQL |
| Data Visualization | Power BI |
| File Format | CSV |
| Version Control | Git & GitHub |

---

# Features

- End-to-End ETL Pipeline
- Medallion Architecture (Bronze, Silver, Gold)
- Delta Lake Storage
- Metadata Tracking
- Automated Workflow using Apache Airflow
- PostgreSQL Data Warehouse
- Star Schema Data Model
- Power BI Business Dashboard
- Modular Project Structure
- Production-style Logging

---

# Project Structure

```
enterprise-retail-lakehouse
│
├── dags/
│   └── retail_pipeline.py
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── jars/
│
├── src/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── common/
│   ├── config/
│   └── logging/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Data Pipeline

## Bronze Layer

Responsibilities

- Ingest raw retail CSV files
- Preserve original data
- Add ingestion metadata
- Store data in Delta Lake format

Metadata captured

- Batch ID
- Pipeline Version
- Source System
- Ingestion Timestamp

---

## Silver Layer

Responsibilities

- Data Cleaning
- Data Type Conversion
- Null Handling
- Duplicate Removal
- Standardization
- Business Transformations

The Silver layer contains clean, validated, analytics-ready datasets.

---

## Gold Layer

Creates dimensional models for analytical reporting.

### Dimension Tables

- dim_customer
- dim_product
- dim_store

### Fact Table

- fact_sales

The Gold layer follows a **Star Schema** for optimized analytical queries.

---

# Data Warehouse

The Gold Layer is loaded into PostgreSQL.

Warehouse Tables

```
dim_customer
dim_product
dim_store
fact_sales
```

Example Record Counts

| Table | Records |
|--------|---------|
| Customers | 1,000 |
| Products | 500 |
| Stores | 20 |
| Sales | 18,142 |

---

# Workflow Orchestration

Apache Airflow automates the complete ETL process.

Pipeline Flow

```
Start
   │
   ▼
Bronze Ingestion
   │
   ▼
Silver Transformation
   │
   ▼
Gold Layer Creation
   │
   ▼
Load to PostgreSQL
   │
   ▼
End
```

The DAG supports

- Scheduled execution
- Retry mechanism
- Task dependency management
- Pipeline monitoring

---

# Power BI Dashboard

The PostgreSQL warehouse is connected to Power BI to create business dashboards.

Dashboard includes

- Total Revenue
- Total Orders
- Sales Trend
- Revenue by Store
- Revenue by Category
- Top Products
- Customer Distribution
- Membership Analysis

---

# Skills Demonstrated

- Data Engineering
- ETL Pipeline Development
- PySpark
- Delta Lake
- Apache Airflow
- PostgreSQL
- Data Warehousing
- Star Schema Modeling
- Workflow Orchestration
- Power BI
- Data Modeling
- Batch Processing

---

# Getting Started

## Clone Repository

```bash
git clone https://github.com/Akshaygn404/enterprise-retail-lakehouse.git
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Initialize Airflow

```bash
export AIRFLOW_HOME=$(pwd)/airflow

airflow db migrate

airflow users create

airflow scheduler

airflow webserver
```

---

## Execute Pipeline

```bash
python -m src.bronze.load_bronze

python -m src.silver.load_silver

python -m src.gold.load_gold
```

Or simply trigger the DAG from the Airflow UI.

---

# Author

**Akshay G N**

B.Tech Computer Science and Engineering

Aspiring Data Engineer

GitHub: https://github.com/Akshaygn404
LinkedIn: https://linkedin.com/in/akshay-gn-5b6932241