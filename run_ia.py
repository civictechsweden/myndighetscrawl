import csv
import os
import pandas as pd

import ia

agency_urls = []

with open("urls.csv", "r") as file:
    agency_urls = [row[0] for row in csv.reader(file)][1:]

data = os.listdir("./data/ia")

for agency_url in agency_urls:
    pdf_urls = []

    if f"{agency_url}.csv" in data:
        print(f"Skipping {agency_url}...")
        continue

    print(f"Searching for {agency_url}...")
    ia.get_pdfs(agency_url)

data = sorted(os.listdir("./data/ia"))

dfs = []
for file in data:
    try:
        df = pd.read_csv("./data/ia/" + file)
        dfs.append(df)
    except pd.errors.EmptyDataError:
        print(f"Empty file: {file}")

combined = pd.concat(dfs)
# combined["archive"] =
print(f"Saving combined.csv with {len(combined)} rows...")
combined.to_csv("combined.csv", index=False)
