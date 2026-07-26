import random
from pathlib import Path

import pandas as pd

from src.config.config import (
    RANDOM_SEED,
    SOURCE_DATA_PATH
)

random.seed(RANDOM_SEED)

products_df = pd.read_csv(f"{SOURCE_DATA_PATH}/products.csv")
stores_df = pd.read_csv(f"{SOURCE_DATA_PATH}/stores.csv")

def generate_inventory():

    inventory = []

    inventory_id = 1

    for _, store in stores_df.iterrows():

        for _, product in products_df.iterrows():

            stock = random.randint(0, 500)

            reorder_level = random.randint(20, 80)

            timestamp = pd.Timestamp.now()

            inventory.append({

                "inventory_id": inventory_id,

                "product_id": product["product_id"],

                "store_id": store["store_id"],

                "stock_quantity": stock,

                "reorder_level": reorder_level,

                "last_updated": timestamp,

                "created_at": timestamp,

                "updated_at": timestamp

            })

            inventory_id += 1

    return pd.DataFrame(inventory)

def save_inventory(df):

    output_path = Path(SOURCE_DATA_PATH)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path / "inventory_stock.csv",
        index=False
    )

    print(f"Generated {len(df)} inventory records successfully.")

if __name__ == "__main__":

    inventory_df = generate_inventory()

    save_inventory(inventory_df)