import random
from pathlib import Path

import pandas as pd

from src.config.config import (
    RANDOM_SEED,
    SOURCE_DATA_PATH,
    RETURN_RATE
)

random.seed(RANDOM_SEED)

orders_df = pd.read_csv(f"{SOURCE_DATA_PATH}/orders.csv")

delivered_orders = orders_df[
    orders_df["order_status"] == "Delivered"
]

return_reasons = [
    "Damaged Product",
    "Wrong Item",
    "Size Issue",
    "Defective",
    "Changed Mind"
]

def generate_returns():

    returns = []

    return_id = 1

    sampled_orders = delivered_orders.sample(
        frac=RETURN_RATE,
        random_state=RANDOM_SEED
    )

    for _, order in sampled_orders.iterrows():

        return_date = pd.to_datetime(order["order_date"]) + pd.Timedelta(
            days=random.randint(1, 15)
        )

        returns.append({

            "return_id": return_id,

            "order_id": order["order_id"],

            "return_date": return_date,

            "return_reason": random.choice(return_reasons),

            "refund_amount": order["total_amount"],

            "created_at": return_date,

            "updated_at": return_date

        })

        return_id += 1

    return pd.DataFrame(returns)


def save_returns(df):

    output_path = Path(SOURCE_DATA_PATH)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path / "returns.csv",
        index=False
    )

    print(f"Generated {len(df)} returns successfully.")

if __name__ == "__main__":

    returns_df = generate_returns()

    save_returns(returns_df)