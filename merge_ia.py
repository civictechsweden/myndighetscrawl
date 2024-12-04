import os
import pandas as pd
import urllib.parse


def filename(url):
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    pdf_name = path.split("/")[-1]

    return pdf_name


def web_url(timestamp, original):
    timestamp_str = str(int(timestamp))
    return f"https://web.archive.org/web/{timestamp_str}/{original}"


data = sorted(os.listdir("./data/ia"))

dfs = []
for file in data:
    try:
        df = pd.read_csv("./data/ia/" + file)
        if not df.empty:
            dfs.append(df)
    except pd.errors.EmptyDataError:
        print(f"Empty file: {file}")

combined = pd.concat(dfs)

combined["archive"] = combined.apply(
    lambda row: web_url(row["timestamp"], row["original"]), axis=1
)

combined["filename"] = combined["original"].apply(filename)


print(f"Saving combined.csv with {len(combined)} rows...")
combined.to_csv("combined.csv", index=False)
combined.to_parquet("combined.parquet", index=False)
