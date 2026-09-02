import pandas as pd
import os

FEATURE_PATH = "data/features"
os.makedirs(FEATURE_PATH, exist_ok=True)

interactions = pd.read_csv("data/processed/interactions_clean.csv")
popularity = pd.read_csv("data/raw/item_popularity.csv")

user_features = interactions.groupby("user_id").size().reset_index(name="interaction_count")

item_features = interactions.groupby("item_id").size().reset_index(name="item_interactions")
item_features = item_features.merge(popularity, on="item_id", how="left")

user_features.to_csv(f"{FEATURE_PATH}/user_features.csv", index=False)
item_features.to_csv(f"{FEATURE_PATH}/item_features.csv", index=False)

print("✅ Features created")