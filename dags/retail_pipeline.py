from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

# ---------------------------------------------------------
# Default Arguments
# ---------------------------------------------------------

default_args = {
    "owner": "Akshay",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

# ---------------------------------------------------------
# DAG Definition
# ---------------------------------------------------------

with DAG(
    dag_id="enterprise_retail_pipeline",
    description="End-to-End Enterprise Retail Lakehouse ETL Pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["Retail", "Spark", "Delta", "PostgreSQL"],
) as dag:

    # ---------------------------------------------------------
    # Start
    # ---------------------------------------------------------

    start = EmptyOperator(
        task_id="start_pipeline"
    )

    # ---------------------------------------------------------
    # Bronze Layer
    # ---------------------------------------------------------

    bronze_ingestion = BashOperator(
        task_id="bronze_ingestion",
        bash_command="""
        cd /Users/akshaygn/Desktop/enterprise-retail-lakehouse &&
        source venv/bin/activate &&
        python -m src.bronze.load_bronze
        """
    )

    # ---------------------------------------------------------
    # Silver Layer
    # ---------------------------------------------------------

    silver_transformation = BashOperator(
        task_id="silver_transformation",
        bash_command="""
        cd /Users/akshaygn/Desktop/enterprise-retail-lakehouse &&
        source venv/bin/activate &&
        python -m src.silver.load_silver
        """
    )

    # ---------------------------------------------------------
    # Gold Layer
    # ---------------------------------------------------------

    gold_data_warehouse = BashOperator(
        task_id="gold_data_warehouse",
        bash_command="""
        cd /Users/akshaygn/Desktop/enterprise-retail-lakehouse &&
        source venv/bin/activate &&
        python -m src.gold.load_gold
        """
    )

    # ---------------------------------------------------------
    # End
    # ---------------------------------------------------------

    end = EmptyOperator(
        task_id="pipeline_completed"
    )

    # ---------------------------------------------------------
    # Pipeline Flow
    # ---------------------------------------------------------

    (
        start
        >> bronze_ingestion
        >> silver_transformation
        >> gold_data_warehouse
        >> end
    )