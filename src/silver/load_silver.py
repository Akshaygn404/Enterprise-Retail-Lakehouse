from src.common.spark_session import create_spark_session

from src.common.logger import get_logger

from src.common.metadata import (
    generate_batch_id,
    add_metadata_columns
)

from src.silver.silver_transform import (
    TABLE_TRANSFORMERS
)

def main():

    logger = get_logger("Silver")

    logger.info("Silver Job Started")

    spark = create_spark_session()

    batch_id = generate_batch_id()

    logger.info(f"Batch ID: {batch_id}")

    try:

        for table_name, transformer in TABLE_TRANSFORMERS.items():

            logger.info(f"Transforming {table_name}...")

            bronze_df = (

                spark.read

                .format("delta")

                .load(

                    f"data/bronze/{table_name}"

                )

            )

            silver_df = transformer(bronze_df)

            

            silver_df = add_metadata_columns(
                silver_df,
                batch_id
            )
            

            silver_df = add_metadata_columns(
                silver_df,
                batch_id
            )

            (

                silver_df.write

                .format("delta")

                .mode("overwrite")

                .save(

                    f"data/silver/{table_name}"

                )

            )

            logger.info(f"{table_name} completed.")

        logger.info("Silver Job Completed Successfully.")

    except Exception as e:

        logger.error(f"Silver Job Failed: {e}")

        raise

    finally:

        spark.stop()

        logger.info("Spark Session Stopped.")


if __name__ == "__main__":

    main()