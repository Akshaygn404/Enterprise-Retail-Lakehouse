from datetime import datetime
from src.config.config import (
    PIPELINE_VERSION,
    SOURCE_SYSTEM
)
from pyspark.sql.functions import (
    current_timestamp,
    lit
)
def generate_batch_id():

    return datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

def add_metadata_columns(
    df,
    batch_id
):

    return (

        df

        .withColumn(
            "batch_id",
            lit(batch_id)
        )

        .withColumn(
            "pipeline_version",
            lit(PIPELINE_VERSION)
        )

        .withColumn(
            "source_system",
            lit(SOURCE_SYSTEM)
        )

        .withColumn(
            "processed_timestamp",
            current_timestamp()
        )

    )