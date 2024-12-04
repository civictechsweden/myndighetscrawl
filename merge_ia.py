import os
import pandas as pd


def filename(urls):
    return urls.str.split("/").str[-1]


def web_url(timestamps, originals):
    return (
        "https://web.archive.org/web/"
        + (timestamps.astype(int).astype(str))
        + "/"
        + originals
    )


data = sorted(os.listdir("./data/ia"))

dfs = []
for file in data:
    try:
        df = pd.read_csv("./data/ia/" + file)
        if not df.empty:
            print(f"Adding: {file}")
            dfs.append(df)
    except pd.errors.EmptyDataError:
        print(f"Empty file: {file}")

print("Concatenating...")
combined = pd.concat(dfs)

print("Adding archive urls...")
combined["archive"] = web_url(combined["timestamp"], combined["original"])

print("Adding filename...")
combined["filename"] = filename(combined["original"])

print(f"Saving combined.csv with {len(combined)} rows...")
combined.to_csv("combined.csv", index=False)
combined.to_parquet("combined.parquet", index=False)

combined = pd.read_parquet("combined.parquet")


def subset(text):
    df = combined[combined["original"].str.contains(text)]
    df = df.sort_values(by="timestamp")
    df.to_csv(f"./csv/{text}.csv", index=False)


subset("reports")
subset("publikation")
subset("rsredovisning")
subset("budgetunderlag")
subset("regleringsbrev")
