import csv
import os

import cc

agency_urls = []

with open("urls.csv", "r") as file:
    agency_urls = [row[0] for row in csv.reader(file)]

pdf_urls = []

data = os.listdir("./data")

for agency_url in agency_urls[1:]:
    if f"{agency_url}.csv" in data:
        continue

    print(f"Searching for {agency_url}...")

    for index in cc.get_collinfo():
        print(f"Searching in {index['name']}")

        items = cc.get_pdf_links(index["cdx-api"], agency_url)

        print(f"Saving {len(items)} items...")
        for item in items:
            item_url = item["url"]
            pdf_urls.append((agency_url, index["id"].replace("CC-MAIN-", ""), item_url))

    with open(f"./data/{agency_url}.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Domain", "Period", "URL"])
        writer.writerows(sorted(list(set(pdf_urls))))
