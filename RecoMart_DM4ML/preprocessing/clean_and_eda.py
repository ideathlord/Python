import pandas as pd
import os

PROCESSED = "data/processed"
os.makedirs(PROCESSED, exist_ok=True)

users = pd.read_csv("data/raw/users.csv")
products = pd.read_csv("data/raw/products.csv")
interactions = pd.read_csv("data/raw/interactions.csv")

interactions = interactions.drop_duplicates()
interactions["timestamp"] = pd.to_datetime(interactions["timestamp"])

interactions.to_csv(f"{PROCESSED}/interactions_clean.csv", index=False)
users.to_csv(f"{PROCESSED}/users_clean.csv", index=False)
products.to_csv(f"{PROCESSED}/products_clean.csv", index=False)

print("✅ Cleaned data saved")