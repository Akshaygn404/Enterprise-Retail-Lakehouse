from src.common.spark_session import create_spark_session

from src.silver.silver_transform import (
    TABLE_TRANSFORMERS
)

spark = create_spark_session()

for table_name, transformer in TABLE_TRANSFORMERS.items():

    print(f"\nTransforming {table_name}...")

    bronze_df = (

        spark.read

        .format("delta")

        .load(

            f"data/bronze/{table_name}"

        )

    )

    silver_df = transformer(bronze_df)

    (

        silver_df.write

        .format("delta")

        .mode("overwrite")

        .save(

            f"data/silver/{table_name}"

        )

    )

    print(f"{table_name} completed.")

spark.stop()

print("\nSilver Transformation Job Completed.")