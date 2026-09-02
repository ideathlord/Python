import urllib.request
import urllib.parse
import json
import pandas as pd
import os

API_KEY = "ef9a748ee6c2d209d2099fb50e9f07f1"

cache = {}

def fetch_data(series_id, save_path):
    # Always save to the 'data' directory inside the project, using only the basename
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(base_dir, exist_ok=True)
    filename = os.path.basename(save_path)
    save_path = os.path.join(base_dir, filename)
    print(f"Saving file to: {save_path}")

    if series_id in cache:
        print(f"Using cached data for series_id: {series_id}")
        return cache[series_id]
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json"
    }
    url = base_url + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url) as resp:
            j = json.load(resp)
            obs = j.get("observations", [])
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return pd.DataFrame(columns=["date", "value"])
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return pd.DataFrame(columns=["date", "value"])
    obs = j["observations"]

    df = pd.DataFrame(obs)[["date", "value"]]
    df["value"] = pd.to_numeric(df["value"], errors='coerce')
    try:
        cache[series_id] = df
        df.to_csv(save_path, index=False)
    except IOError as e:
        print(f"Error saving file {save_path}: {e}")
    return df

if __name__ == "__main__":
    fetch_data("GASREGW", "data/gas_prices.csv")
    fetch_data("CPIAUCSL", "data/cpi_data.csv")
    print("fred downloaded")
