import logging

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

interactions = pd.read_csv("data/processed/interactions_clean.csv")

le_user = LabelEncoder()
le_item = LabelEncoder()

interactions["user_enc"] = le_user.fit_transform(interactions["user_id"])
interactions["item_enc"] = le_item.fit_transform(interactions["item_id"])

user_item_matrix = pd.pivot_table(
    interactions,
    index="user_enc",
    columns="item_enc",
    aggfunc="size",
    fill_value=0,
)

similarity = cosine_similarity(user_item_matrix)

logging.info("num_users=%d", user_item_matrix.shape[0])
logging.info("num_items=%d", user_item_matrix.shape[1])

print("✅ Model trained & metrics logged")
