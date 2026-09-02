import pandas as pd
import random
import os

RAW_PATH = "data/raw"
os.makedirs(RAW_PATH, exist_ok=True)

def fake_popularity_api(items):
    return pd.DataFrame({
        "item_id": items,
        "popularity_score": [round(random.uniform(0, 1), 2) for _ in items]
    })

if __name__ == "__main__":
    products = pd.read_csv(f"{RAW_PATH}/products.csv")
    popularity = fake_popularity_api(products["item_id"].tolist())
    popularity.to_csv(f"{RAW_PATH}/item_popularity.csv", index=False)

    print("✅ Fake API data ingested")