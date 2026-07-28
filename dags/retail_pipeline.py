from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator



default_args = {
    "owner": "Akshay",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}



with DAG(
    dag_id="enterprise_retail_pipeline",
    description="End-to-End Enterprise Retail Lakehouse ETL Pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["Retail", "Spark", "Delta", "PostgreSQL"],
) as dag:



    start = EmptyOperator(
        task_id="start_pipeline"
    )


    bronze_ingestion = BashOperator(
        task_id="bronze_ingestion",
        bash_command="""
        cd /Users/akshaygn/Desktop/enterprise-retail-lakehouse &&
        source venv/bin/activate &&
        python -m src.bronze.load_bronze
        """
    )

  
    silver_transformation = BashOperator(
        task_id="silver_transformation",
        bash_command="""
        cd /Users/akshaygn/Desktop/enterprise-retail-lakehouse &&
        source venv/bin/activate &&
        python -m src.silver.load_silver
        """
    )

  

    gold_data_warehouse = BashOperator(
        task_id="gold_data_warehouse",
        bash_command="""
        cd /Users/akshaygn/Desktop/enterprise-retail-lakehouse &&
        source venv/bin/activate &&
        python -m src.gold.load_gold
        """
    )



    end = EmptyOperator(
        task_id="pipeline_completed"
    )

  

    (
        start
        >> bronze_ingestion
        >> silver_transformation
        >> gold_data_warehouse
        >> end
    )