import random
from pathlib import Path

import pandas as pd

from src.config.config import (
    RANDOM_SEED,
    SOURCE_DATA_PATH
)

random.seed(RANDOM_SEED)
orders_df = pd.read_csv(f"{SOURCE_DATA_PATH}/orders.csv")

products_df = pd.read_csv(f"{SOURCE_DATA_PATH}/products.csv")

def generate_order_items():

    order_items = []

    order_item_id = 1

    order_totals = {}

    for _, order in orders_df.iterrows():

        num_products = random.randint(1, 5)

        sampled_products = products_df.sample(num_products)

        total_amount = 0

        for _, product in sampled_products.iterrows():

            quantity = random.randint(1, 3)

            unit_price = product["selling_price"]

            discount = round(random.uniform(0, 0.20), 2)

            final_price = round(
                quantity * unit_price * (1 - discount),
                2
            )

            total_amount += final_price

            order_items.append({

                "order_item_id": order_item_id,

                "order_id": order["order_id"],

                "product_id": product["product_id"],

                "quantity": quantity,

                "unit_price": unit_price,

                "discount": discount,

                "final_price": final_price,

                "created_at": order["created_at"],

                "updated_at": order["updated_at"]

            })

            order_item_id += 1

        order_totals[order["order_id"]] = round(total_amount, 2)

    return pd.DataFrame(order_items), order_totals

def update_orders(order_totals):

    orders_df["total_amount"] = orders_df["order_id"].map(order_totals)

    orders_df.to_csv(
        f"{SOURCE_DATA_PATH}/orders.csv",
        index=False
    )

def save_order_items(df):

    output_path = Path(SOURCE_DATA_PATH)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path / "order_items.csv",
        index=False
    )

    print(f"Generated {len(df)} order items successfully.")

if __name__ == "__main__":

    order_items_df, totals = generate_order_items()

    save_order_items(order_items_df)

    update_orders(totals)