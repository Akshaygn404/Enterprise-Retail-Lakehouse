from src.common.spark_session import create_spark_session

from src.common.metadata import (
    generate_batch_id
)

from src.common.logger import (
    get_logger
)

from src.bronze.bronze_ingestion import (
    load_to_bronze
)


TABLES = [
    "customers",
    "products",
    "stores",
    "orders",
    "order_items",
    "inventory_stock",
    "returns"
]


def main():

    logger = get_logger("Bronze")

    logger.info("Bronze Job Started")

    spark = create_spark_session()

    batch_id = generate_batch_id()

    logger.info(f"Batch ID: {batch_id}")

    try:

        for table in TABLES:

            logger.info(f"Loading {table}...")

            load_to_bronze(
                spark,
                table,
                batch_id
            )

            logger.info(f"{table} loaded successfully.")

        logger.info("Bronze Job Completed Successfully.")

    except Exception as e:

        logger.error(f"Bronze Job Failed: {e}")

        raise

    finally:

        spark.stop()

        logger.info("Spark Session Stopped.")


if __name__ == "__main__":

    main()