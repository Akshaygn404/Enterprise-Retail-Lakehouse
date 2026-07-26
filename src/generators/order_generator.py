import random
from pathlib import Path

import pandas as pd
from faker import Faker

from src.config.config import (
    NUM_ORDERS,
    RANDOM_SEED,
    SOURCE_DATA_PATH
)

fake = Faker("en_IN")

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

customers_df = pd.read_csv(f"{SOURCE_DATA_PATH}/customers.csv")
stores_df = pd.read_csv(f"{SOURCE_DATA_PATH}/stores.csv")

customer_ids = customers_df["customer_id"].tolist()
store_ids = stores_df["store_id"].tolist()

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking"
]

payment_weights = [40, 20, 20, 10, 10]

order_statuses = [
    "Delivered",
    "Shipped",
    "Pending",
    "Cancelled"
]

status_weights = [80, 10, 5, 5]

source_systems = [
    "WEB",
    "MOBILE",
    "STORE"
]

source_weights = [45, 35, 20]

def generate_orders():

    orders = []

    for order_id in range(1, NUM_ORDERS + 1):

        order_date = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        created_at = order_date

        updated_at = fake.date_time_between(
            start_date=created_at,
            end_date="now"
        )

        orders.append({

            "order_id": order_id,

            "customer_id": random.choice(customer_ids),

            "store_id": random.choice(store_ids),

            "order_date": order_date,

            "payment_method": random.choices(
                payment_methods,
                weights=payment_weights,
                k=1
            )[0],

            "order_status": random.choices(
                order_statuses,
                weights=status_weights,
                k=1
            )[0],

            # Will be updated after generating order_items
            "total_amount": 0.0,

            "source_system": random.choices(
                source_systems,
                weights=source_weights,
                k=1
            )[0],

            "created_at": created_at,

            "updated_at": updated_at

        })

    return pd.DataFrame(orders)

def save_orders(df):

    output_path = Path(SOURCE_DATA_PATH)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path / "orders.csv",
        index=False
    )

    print(f"Generated {len(df)} orders successfully.")

if __name__ == "__main__":

    orders_df = generate_orders()

    save_orders(orders_df)