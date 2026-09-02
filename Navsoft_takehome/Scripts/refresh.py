import pandas as pd
from sales_generate import generate_sales_data
from api_call import fetch_data
from check_data_anamoly import check_data, write_log

def run_pipeline():
    s = generate_sales_data()
    g = fetch_data("GASREGW", "/data/gas_prices.csv")
    c = fetch_data("CPIAUCSL", "/data/cpi_data.csv")

    s["week_start_date"] = pd.to_datetime(s["week_start_date"])
    g["date"] = pd.to_datetime(g["date"])
    c["date"] = pd.to_datetime(c["date"])

    s = s.merge(
        g.rename(columns={"date": "week_start_date", "value": "avg_gas_price"}),
        on="week_start_date",
        how="left"
    )

    s = s.merge(
        c.rename(columns={"date": "week_start_date", "value": "cpi"}),
        on="week_start_date",
        how="left"
    )

    import os
    # Ensure the 'data' directory exists for saving the merged data file
    os.makedirs("data", exist_ok=True)
    s.to_csv("data/merged_data.csv", index=False)

    problems = check_data(s)
    if problems:
        write_log(problems)
        print("problems logged")
    else:
        print("done ok")

if __name__ == "__main__":
    run_pipeline()
