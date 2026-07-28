from src.config.config import SOURCE_DATA_PATH
from src.common.metadata import add_metadata_columns


def load_to_bronze(spark, table_name, batch_id):

    source_file = f"{SOURCE_DATA_PATH}/{table_name}.csv"
    bronze_path = f"data/bronze/{table_name}"

    print(f"\n{'=' * 60}")
    print(f"Loading {table_name.upper()}")
    print(f"{'=' * 60}")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(source_file)
    )

    df = add_metadata_columns(
        df,
        batch_id
    )

    print(f"Total Records : {df.count()}")

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .save(bronze_path)
    )

    print(f"{table_name} loaded successfully.")