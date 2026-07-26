import random
from pathlib import Path

import pandas as pd
from faker import Faker

from src.config.config import (
    NUM_PRODUCTS,
    RANDOM_SEED,
    SOURCE_DATA_PATH
)

fake = Faker("en_IN")

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

categories = [
    "Electronics",
    "Clothing",
    "Groceries",
    "Home & Kitchen",
    "Sports",
    "Beauty",
    "Books"
]

brands = [
    "Samsung",
    "Apple",
    "Nike",
    "Adidas",
    "Sony",
    "LG",
    "Boat",
    "Lenovo",
    "HP",
    "Puma"
]

suppliers = [
    "Supplier A",
    "Supplier B",
    "Supplier C",
    "Supplier D",
    "Supplier E"
]

def generate_products():

    products = []

    for product_id in range(1, NUM_PRODUCTS + 1):

        cost_price = round(random.uniform(100, 50000), 2)

        markup = random.uniform(0.10, 0.40)

        selling_price = round(cost_price * (1 + markup), 2)

        launch_date = fake.date_between(
            start_date="-5y",
            end_date="today"
        )

        created_at = fake.date_time_between(
            start_date=launch_date,
            end_date="now"
        )

        updated_at = fake.date_time_between(
            start_date=created_at,
            end_date="now"
        )

        category = random.choice(categories)

        brand = random.choice(brands)

        product_name = f"{brand} {category} Product {product_id}"

        products.append({

            "product_id": product_id,

            "product_name": product_name,

            "category": category,

            "brand": brand,

            "cost_price": cost_price,

            "selling_price": selling_price,

            "supplier_name": random.choice(suppliers),

            "launch_date": launch_date,

            "is_active": random.choices(
                [True, False],
                weights=[95, 5],
                k=1
            )[0],

            "created_at": created_at,

            "updated_at": updated_at

        })

    return pd.DataFrame(products)

def save_products(df):

    output_path = Path(SOURCE_DATA_PATH)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path / "products.csv",
        index=False
    )

    print(f"Generated {len(df)} products successfully.")


if __name__ == "__main__":

    products_df = generate_products()

    save_products(products_df)