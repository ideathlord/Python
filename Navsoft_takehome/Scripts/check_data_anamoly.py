import pandas as pd

def check_data(df):
    problems = []

    if df.isna().sum().sum() > 0:
        problems.append("missing data exists")

    u = df["units_sold"]
    mean = u.mean()
    std = u.std()

    spikes = df[(u > mean + 3*std) | (u < mean - 3*std)]
    if len(spikes) > 0:
        problems.append("spikes found")

    return problems

def write_log(problems):
    with open("data/alerts.log", "a") as f:
        for p in problems:
            f.write(p + "\n")

if __name__ == "__main__":
    df = pd.read_csv("data/merged_data.csv")
    issues = check_data(df)
    if issues:
        write_log(issues)
        print("issues found")
    else:
        print("ok")
