import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42)

RAW_PATH = "data/raw"
os.makedirs(RAW_PATH, exist_ok=True)

def generate_users(n=100):
    return pd.DataFrame({
        "user_id": [f"user_{i}" for i in range(1, n+1)],
        "age": [random.randint(18, 60) for _ in range(n)],
        "city": [fake.city() for _ in range(n)]
    })

def generate_products(n=50):
    categories = ["Electronics", "Clothing", "Books", "Home"]
    return pd.DataFrame({
        "item_id": [f"item_{i}" for i in range(1, n+1)],
        "category": [random.choice(categories) for _ in range(n)],
        "price": [random.randint(200, 5000) for _ in range(n)]
    })

def generate_interactions(users, products, n=1000):
    rows = []
    for _ in range(n):
        rows.append({
            "user_id": random.choice(users["user_id"]),
            "item_id": random.choice(products["item_id"]),
            "event_type": random.choice(["view", "click", "purchase"]),
            "timestamp": datetime.now() - timedelta(days=random.randint(0, 30))
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    users = generate_users()
    products = generate_products()
    interactions = generate_interactions(users, products)

    users.to_csv(f"{RAW_PATH}/users.csv", index=False)
    products.to_csv(f"{RAW_PATH}/products.csv", index=False)
    interactions.to_csv(f"{RAW_PATH}/interactions.csv", index=False)

    print("✅ CSV data generated")