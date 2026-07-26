from pyspark.sql.functions import col


def build_dim_customer(df):

    return (

        df

        .select(

            "customer_id",

            "first_name",

            "last_name",

            "gender",

            "city",

            "state",

            "country",

            "membership_type",

            "registration_date",

            "is_active"

        )

    )

def build_dim_product(df):

    return (

        df

        .select(

            "product_id",

            "product_name",

            "category",

            "brand",

            "supplier_name",

            "launch_date",

            "is_active"

        )

    )

def build_dim_store(df):

    return (

        df

        .select(

            "store_id",

            "store_name",

            "city",

            "state",

            "region",

            "manager_name",

            "store_type",

            "opening_date",

            "is_active"

        )

    )

from pyspark.sql.functions import col, round


def build_fact_sales(orders_df, order_items_df):

    fact_sales = (

        order_items_df.alias("oi")

        .join(

            orders_df.alias("o"),

            col("oi.order_id") == col("o.order_id"),

            "inner"

        )

        .select(

            col("oi.order_item_id"),

            col("oi.order_id"),

            col("o.customer_id"),

            col("o.store_id"),

            col("oi.product_id"),

            col("o.order_date"),

            col("oi.quantity"),

            col("oi.unit_price"),

            col("oi.discount"),

            col("oi.final_price")

        )

    )

    fact_sales = (

        fact_sales

        .withColumn(

            "gross_sales",

            round(

                col("quantity") * col("unit_price"),

                2

            )

        )

        .withColumn(

            "discount_amount",

            round(

                col("gross_sales") * col("discount"),

                2

            )

        )

        .withColumn(

            "net_sales",

            col("final_price")

        )

    )

    return fact_sales

TABLE_BUILDERS = {

    "dim_customer": build_dim_customer,

    "dim_product": build_dim_product,

    "dim_store": build_dim_store,

    # "fact_sales": build_fact_sales

}