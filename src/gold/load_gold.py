from src.common.spark_session import create_spark_session

from src.gold.gold_transform import (
    TABLE_BUILDERS,
    build_fact_sales
)

spark = create_spark_session()

SOURCE_TABLES = {
    "dim_customer": "customers",
    "dim_product": "products",
    "dim_store": "stores"
}

for gold_table, builder in TABLE_BUILDERS.items():

    print(f"\nBuilding {gold_table}...")

    silver_table = SOURCE_TABLES[gold_table]

    silver_df = (

        spark.read

        .format("delta")

        .load(f"data/silver/{silver_table}")

    )

    gold_df = builder(silver_df)

    (

        gold_df.write

        .format("delta")

        .mode("overwrite")

        .save(f"data/gold/{gold_table}")

    )

    print(f"{gold_table} completed.")

orders_df = (

    spark.read

    .format("delta")

    .load("data/silver/orders")

)

order_items_df = (

    spark.read

    .format("delta")

    .load("data/silver/order_items")

)

fact_sales = build_fact_sales(
    orders_df,
    order_items_df
)

(

    fact_sales.write

    .format("delta")

    .mode("overwrite")

    .save("data/gold/fact_sales")

)

print("fact_sales completed.")

spark.stop()

print("\nGold Build Job Completed.")