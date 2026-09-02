import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data():
    np.random.seed(1)

    start = datetime(2024, 1, 1)
    while start.weekday() != 6:
        start = start - timedelta(days=1)

    weeks = []
    for i in range(52):
        weeks.append(start + timedelta(weeks=i))

    product_ids = []
    product_names = []
    for i in range(1, 51):
        product_ids.append("P" + str(i))
        product_names.append("Product_" + str(i))

    data = []
    for w in weeks:
        for i in range(50):
            units = np.random.randint(50, 200)
            price = round(np.random.uniform(5, 50), 2)
            discount = np.random.choice([0, 5, 10, 15])
            revenue = units * price * (1 - discount/100)

            data.append([
                w.date(),
                product_ids[i],
                product_names[i],
                units,
                price,
                discount,
                revenue,
                "USA"
            ])

    df = pd.DataFrame(data, columns=[
        "week_start_date",
        "product_id",
        "product_name",
        "units_sold",
        "price",
        "discount_pct",
        "revenue",
        "region"
    ])

    df.to_csv("data/sales_data.csv", index=False)
    return df

if __name__ == "__main__":
    generate_sales_data()
    print("sales created")
