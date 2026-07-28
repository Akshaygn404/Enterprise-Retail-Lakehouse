POSTGRES_URL = "jdbc:postgresql://localhost:5432/retail_warehouse"

POSTGRES_PROPERTIES = {
    "user": "akshaygn",
    "password": "",
    "driver": "org.postgresql.Driver"
}


def write_to_postgres(df, table_name):

    (

        df.write

        .mode("overwrite")

        .jdbc(

            url=POSTGRES_URL,

            table=table_name,

            properties=POSTGRES_PROPERTIES

        )

    )