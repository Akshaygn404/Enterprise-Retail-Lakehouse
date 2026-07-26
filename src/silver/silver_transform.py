from pyspark.sql.functions import col, to_timestamp

from src.silver.common_transformations import (
    apply_common_transformations
)
from src.silver.common_transformations import (
    apply_common_transformations,
    log_validation_metrics
)


def standardize_customers(df):

    return (

        df

        .withColumn(
            "registration_date",
            col("registration_date").cast("date")
        )

        .withColumn(
            "created_at",
            to_timestamp("created_at")
        )

        .withColumn(
            "updated_at",
            to_timestamp("updated_at")
        )

    )


def validate_customers(df):

    return df.filter(

        col("customer_id").isNotNull()

    )


def transform_customers(df):

    df = apply_common_transformations(df)

    df = standardize_customers(df)

    before_validation = df

    df = validate_customers(df)

    df = log_validation_metrics(
        before_validation,
        df,
        "customers"
    )

    return df


def standardize_products(df):

    return (

        df

        .withColumn(
            "launch_date",
            col("launch_date").cast("date")
        )

        .withColumn(
            "created_at",
            to_timestamp("created_at")
        )

        .withColumn(
            "updated_at",
            to_timestamp("updated_at")
        )

    )

def validate_products(df):

    return (

        df

        .filter(col("product_id").isNotNull())

        .filter(col("brand").isNotNull())

        .filter(col("category").isNotNull())

        .filter(col("cost_price") > 0)

        .filter(col("selling_price") > col("cost_price"))

    )

def transform_products(df):

    df = apply_common_transformations(df)

    df = standardize_products(df)

    before_validation = df

    df = validate_products(df)

    df = log_validation_metrics(
        before_validation,
        df,
        "products"
    )

    return df


def standardize_orders(df):

    return (

        df

        .withColumn(
            "order_date",
            to_timestamp("order_date")
        )

        .withColumn(
            "created_at",
            to_timestamp("created_at")
        )

        .withColumn(
            "updated_at",
            to_timestamp("updated_at")
        )

    )

VALID_PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking"
]

VALID_ORDER_STATUS = [
    "Delivered",
    "Shipped",
    "Pending",
    "Cancelled"
]


def validate_orders(df):

    return (

        df

        .filter(col("order_id").isNotNull())

        .filter(col("customer_id").isNotNull())

        .filter(col("store_id").isNotNull())

        .filter(col("total_amount") >= 0)

        .filter(col("payment_method").isin(VALID_PAYMENT_METHODS))

        .filter(col("order_status").isin(VALID_ORDER_STATUS))

    )

def transform_orders(df):

    df = apply_common_transformations(df)

    df = standardize_orders(df)

    before_validation = df

    df = validate_orders(df)

    df = log_validation_metrics(
        before_validation,
        df,
        "orders"
    )

    return df



def standardize_order_items(df):

    return (

        df

        .withColumn(
            "created_at",
            to_timestamp("created_at")
        )

        .withColumn(
            "updated_at",
            to_timestamp("updated_at")
        )

    )


def validate_order_items(df):

    return (

        df

        .filter(col("order_item_id").isNotNull())

        .filter(col("order_id").isNotNull())

        .filter(col("product_id").isNotNull())

        .filter(col("quantity") > 0)

        .filter(col("unit_price") > 0)

        .filter(
            (col("discount") >= 0) &
            (col("discount") <= 1)
        )

        .filter(col("final_price") > 0)

    )

def transform_order_items(df):

    df = apply_common_transformations(df)

    df = standardize_order_items(df)

    before_validation = df

    df = validate_order_items(df)

    df = log_validation_metrics(
        before_validation,
        df,
        "order_items"
    )

    return df

def standardize_inventory(df):

    return (

        df

        .withColumn(
            "last_updated",
            to_timestamp("last_updated")
        )

        .withColumn(
            "created_at",
            to_timestamp("created_at")
        )

        .withColumn(
            "updated_at",
            to_timestamp("updated_at")
        )

    )

def validate_inventory(df):

    return (

        df

        .filter(col("inventory_id").isNotNull())

        .filter(col("product_id").isNotNull())

        .filter(col("store_id").isNotNull())

        .filter(col("stock_quantity") >= 0)

        .filter(col("reorder_level") >= 0)

    )

def transform_inventory(df):

    df = apply_common_transformations(df)

    df = standardize_inventory(df)

    before_validation = df

    df = validate_inventory(df)

    df = log_validation_metrics(
        before_validation,
        df,
        "inventory_stock"
    )

    return df


def standardize_returns(df):

    return (

        df

        .withColumn(
            "return_date",
            to_timestamp("return_date")
        )

        .withColumn(
            "created_at",
            to_timestamp("created_at")
        )

        .withColumn(
            "updated_at",
            to_timestamp("updated_at")
        )

    )

def validate_returns(df):

    return (

        df

        .filter(col("return_id").isNotNull())

        .filter(col("order_id").isNotNull())

        .filter(col("refund_amount") >= 0)

    )

def transform_returns(df):

    df = apply_common_transformations(df)

    df = standardize_returns(df)

    before_validation = df

    df = validate_returns(df)

    df = log_validation_metrics(
        before_validation,
        df,
        "returns"
    )

    return df

def standardize_stores(df):

    return (

        df

        .withColumn(
            "opening_date",
            col("opening_date").cast("date")
        )

        .withColumn(
            "created_at",
            to_timestamp("created_at")
        )

        .withColumn(
            "updated_at",
            to_timestamp("updated_at")
        )

    )

def validate_stores(df):

    return (

        df

        .filter(col("store_id").isNotNull())

        .filter(col("store_name").isNotNull())

        .filter(col("city").isNotNull())

        .filter(col("state").isNotNull())

        .filter(col("region").isNotNull())

    )

def transform_stores(df):

    df = apply_common_transformations(df)

    df = standardize_stores(df)

    before_validation = df

    df = validate_stores(df)

    df = log_validation_metrics(
        before_validation,
        df,
        "stores"
    )

    return df

TABLE_TRANSFORMERS = {

    "customers": transform_customers,

    "products": transform_products,

    "stores": transform_stores,

    "orders": transform_orders,

    "order_items": transform_order_items,

    "inventory_stock": transform_inventory,

    "returns": transform_returns

}