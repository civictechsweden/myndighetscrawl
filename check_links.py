import os
import requests
import pandas as pd

DATA = "./data"

verified_links = []
for filename in sorted(os.listdir(DATA)):
    file_path = os.path.join(DATA, filename)
    if filename.endswith('.csv'):
        df = pd.read_csv(file_path)

        print(f"Opened {filename}")
        for _, row in df.iterrows():
            if "2024" in row["Period"]:
                print(f"Trying {row["URL"]}")
                response = requests.head(row["URL"])
                print(response.status_code)
