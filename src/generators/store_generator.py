import random
from pathlib import Path

import pandas as pd
from faker import Faker

from src.config.config import (
    NUM_STORES,
    RANDOM_SEED,
    SOURCE_DATA_PATH
)

fake = Faker("en_IN")

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

regions = {
    "Karnataka": "South",
    "Tamil Nadu": "South",
    "Kerala": "South",
    "Telangana": "South",
    "Andhra Pradesh": "South",

    "Maharashtra": "West",
    "Gujarat": "West",
    "Goa": "West",

    "Delhi": "North",
    "Punjab": "North",
    "Haryana": "North",
    "Rajasthan": "North",

    "West Bengal": "East",
    "Odisha": "East",
    "Bihar": "East"
}

store_types = [
    "Mall",
    "High Street",
    "Outlet"
]

def generate_stores():

    stores = []

    states = list(regions.keys())

    for store_id in range(1, NUM_STORES + 1):

        state = random.choice(states)

        region = regions[state]

        created_at = fake.date_time_between(
            start_date="-10y",
            end_date="now"
        )

        updated_at = fake.date_time_between(
            start_date=created_at,
            end_date="now"
        )

        stores.append({

            "store_id": store_id,

            "store_name": f"RetailX Store {store_id}",

            "city": fake.city(),

            "state": state,

            "region": region,

            "opening_date": fake.date_between(
                start_date="-10y",
                end_date="today"
            ),

            "manager_name": fake.name(),

            "store_type": random.choice(store_types),

            "is_active": random.choices(
                [True, False],
                weights=[95, 5],
                k=1
            )[0],

            "created_at": created_at,

            "updated_at": updated_at

        })

    return pd.DataFrame(stores)


def save_stores(df):

    output_path = Path(SOURCE_DATA_PATH)

    output_path.mkdir(
        parents=True,
        exist_ok=True)

    df.to_csv(
        output_path / "stores.csv",
        index=False
    )

    print(f"Generated {len(df)} stores successfully.")


if __name__ == "__main__":

    stores_df = generate_stores()

    save_stores(stores_df)