from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .master("local[1]")
    .appName("Delta Test")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("SUCCESS")

spark.stop()