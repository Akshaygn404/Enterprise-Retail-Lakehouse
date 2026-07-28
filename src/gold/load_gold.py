from src.common.spark_session import create_spark_session

from src.common.logger import get_logger

from src.common.metadata import (
    generate_batch_id,
    add_metadata_columns
)

from src.gold.gold_transform import (
    TABLE_BUILDERS,
    build_fact_sales
)
from src.common.postgres import write_to_postgres


SOURCE_TABLES = {

    "dim_customer": "customers",

    "dim_product": "products",

    "dim_store": "stores"

}


def main():

    logger = get_logger("Gold")

    logger.info("Gold Job Started")

    spark = create_spark_session()

    batch_id = generate_batch_id()

    logger.info(f"Batch ID: {batch_id}")

    try:

        for gold_table, builder in TABLE_BUILDERS.items():

            logger.info(f"Building {gold_table}...")

            silver_table = SOURCE_TABLES[gold_table]

            silver_df = (

                spark.read

                .format("delta")

                .load(

                    f"data/silver/{silver_table}"

                )

            )

            gold_df = builder(silver_df)

            gold_df = add_metadata_columns(
                gold_df,
                batch_id
            )

            (

                gold_df.write

                .format("delta")

                .mode("overwrite")

                .save(

                    f"data/gold/{gold_table}"

                )

            )
            write_to_postgres(
                gold_df,
                gold_table
            )

            logger.info(f"{gold_table} completed.")

        logger.info("Building fact_sales...")

        orders_df = (

            spark.read

            .format("delta")

            .load(

                "data/silver/orders"

            )

        )

        order_items_df = (

            spark.read

            .format("delta")

            .load(

                "data/silver/order_items"

            )

        )

        fact_sales = build_fact_sales(
            orders_df,
            order_items_df
        )

        fact_sales = add_metadata_columns(
            fact_sales,
            batch_id
        )

        (

            fact_sales.write

            .format("delta")

            .mode("overwrite")

            .save(

                "data/gold/fact_sales"

            )

        )
        write_to_postgres(
            fact_sales,
            "fact_sales"
        )

        logger.info("fact_sales completed.")

        logger.info("Gold Job Completed Successfully.")

    except Exception as e:

        logger.error(f"Gold Job Failed: {e}")

        raise

    finally:

        spark.stop()

        logger.info("Spark Session Stopped.")


if __name__ == "__main__":

    main()