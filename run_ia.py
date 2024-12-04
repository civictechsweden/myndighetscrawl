import csv
import os
import pandas as pd

import ia

agency_urls = []

with open("urls.csv", "r") as file:
    agency_urls = [row[0] for row in csv.reader(file)][1:]

data = os.listdir("./data/ia")

for agency_url in agency_urls:
    if f"{agency_url}.csv" in data:
        print(f"Skipping {agency_url}...")
        continue

    print(f"Searching for {agency_url}...")
    ia.get_pdfs(agency_url)
