import pandas as pd

def validate(df, name):
    print(f"\nValidating {name}")
    print("Missing values:\n", df.isnull().sum())
    print("Duplicates:", df.duplicated().sum())

if __name__ == "__main__":
    validate(pd.read_csv("data/raw/users.csv"), "Users")
    validate(pd.read_csv("data/raw/products.csv"), "Products")
    validate(pd.read_csv("data/raw/interactions.csv"), "Interactions")