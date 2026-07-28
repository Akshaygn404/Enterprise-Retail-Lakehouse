from pathlib import Path
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


def create_spark_session():

    project_root = Path(__file__).resolve().parents[2]

    jdbc_jar = project_root / "jars" / "postgresql-42.7.7.jar"

    print(f"Loading JDBC Driver: {jdbc_jar}")

    builder = (

        SparkSession.builder

        .appName("Enterprise Retail Lakehouse")

        .master("local[*]")

        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension"
        )

        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        )

        .config(
            "spark.driver.host",
            "127.0.0.1"
        )

        .config(
            "spark.driver.bindAddress",
            "127.0.0.1"
        )

        .config(
            "spark.jars",
            str(jdbc_jar)
        )

    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    return spark