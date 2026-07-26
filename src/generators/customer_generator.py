import random
from pathlib import Path

import pandas as pd
from faker import Faker

from src.config.config import (
    NUM_CUSTOMERS,
    RANDOM_SEED,
    SOURCE_DATA_PATH
)

fake = Faker("en_IN")

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

membership_types = [
    "Regular",
    "Silver",
    "Gold",
    "Platinum"
]

membership_weights = [
    70,
    15,
    10,
    5
]
source_systems = [
    "WEB",
    "MOBILE",
    "STORE"
]

source_weights = [
    45,
    35,
    20
]

def generate_customers():

    customers = []

    for customer_id in range(1, NUM_CUSTOMERS + 1):

        registration_date = fake.date_between(
            start_date="-5y",
            end_date="today"
        )

        created_at = fake.date_time_between(
            start_date=registration_date,
            end_date="now"
        )

        updated_at = fake.date_time_between(
            start_date=created_at,
            end_date="now"
        )

        customers.append({

            "customer_id": customer_id,

            "first_name": fake.first_name(),

            "last_name": fake.last_name(),

            "gender": random.choice(
                ["Male", "Female"]
            ),

            "email": fake.unique.email(),

            "phone": fake.phone_number(),

            "city": fake.city(),

            "state": fake.state(),

            "country": "India",

            "pincode": fake.postcode(),

            "registration_date": registration_date,

            "membership_type": random.choices(
                membership_types,
                weights=membership_weights,
                k=1
            )[0],

            "is_active": random.choices(
                [True, False],
                weights=[95, 5],
                k=1
            )[0],

            "source_system": random.choices(
                source_systems,
                weights=source_weights,
                k=1
            )[0],

            "created_at": created_at,

            "updated_at": updated_at

        })

    return pd.DataFrame(customers)

def save_customers(df):

    output_path = Path(SOURCE_DATA_PATH)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path / "customers.csv",
        index=False
    )

    print(
        f"Generated {len(df)} customers successfully."
    )

if __name__ == "__main__":

    customers_df = generate_customers()

    save_customers(customers_df)