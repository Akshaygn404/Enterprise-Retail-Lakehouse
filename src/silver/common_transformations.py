from pyspark.sql.functions import col, initcap, trim
from pyspark.sql.types import StringType
from src.config.config import TEXT_STANDARDIZATION_EXCLUDED_COLUMNS 

def remove_duplicates(df):

    return df.dropDuplicates()


def get_string_columns(df):

    return [
        field.name
        for field in df.schema.fields
        if isinstance(field.dataType, StringType)
    ]


def trim_strings(df):

    string_columns = get_string_columns(df)

    for column in string_columns:

        df = df.withColumn(
            column,
            trim(col(column))
        )

    return df


def standardize_text(df):

    string_columns = get_string_columns(df)

    for column in string_columns:
        if column in TEXT_STANDARDIZATION_EXCLUDED_COLUMNS:
            continue

        df = df.withColumn(
            column,
            initcap(col(column))
        )

    return df


def log_record_count(df, stage):

    print(f"{stage}: {df.count()} records")

    return df


def apply_common_transformations(df):

    df = log_record_count(df, "Before Transformations")

    df = remove_duplicates(df)
    df = log_record_count(df, "After Removing Duplicates")

    df = trim_strings(df)

    df = standardize_text(df)

    return df

def log_validation_metrics(before_df, after_df, table_name):

    before_count = before_df.count()

    after_count = after_df.count()

    rejected_count = before_count - after_count

    print(f"\n{table_name.upper()} VALIDATION METRICS")
    print("-" * 40)
    print(f"Records Before Validation : {before_count}")
    print(f"Records After Validation  : {after_count}")
    print(f"Rejected Records          : {rejected_count}")

    return after_df