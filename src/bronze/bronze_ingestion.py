from src.config.config import SOURCE_DATA_PATH


def load_to_bronze(spark, table_name):

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

    print(f"Total Records : {df.count()}")

    df.printSchema()

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .save(bronze_path)
    )

    print(f"✓ {table_name} loaded successfully.")