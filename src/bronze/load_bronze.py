from src.bronze.bronze_ingestion import load_to_bronze
from src.common.spark_session import create_spark_session

spark = create_spark_session()

tables = [
    "customers",
    "products",
    "stores",
    "orders",
    "order_items",
    "inventory_stock",
    "returns"
]

for table in tables:
    load_to_bronze(spark, table)

spark.stop()

print("\nBronze Layer Loaded Successfully!")