import pandas as pd
import os
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse
import time

session = requests.Session()
adapter = HTTPAdapter(max_retries=3)
session.mount("http://", adapter)
session.mount("https://", adapter)

df = pd.read_csv("csv/rsredovisning.csv")
os.makedirs("annual_reports", exist_ok=True)

for index, row in df.iterrows():
    full_url = row["original"]
    base_domain = full_url.replace("http://", "").replace("https://", "")
    base_domain = base_domain.split("/")[0]
    base_domain = base_domain.split(":")[0]
    base_domain = ".".join(base_domain.split(".")[-2:])
    filename = f"{base_domain}_{index}_{row["filename"]}"
    filepath = os.path.join("annual_reports", filename)

    if os.path.exists(filepath):
        print(f"Skipping {filename}")
        continue

    print(f"Downloading {row["archive"]}...")
    try:
        response = session.get(row["archive"])
    except Exception as e:
        print("Error: skipping...")
        print(e)
        time.sleep(5)
        continue

    if response.status_code == 200:
        file_path = filepath
        with open(file_path, "wb") as f:
            f.write(response.content)
