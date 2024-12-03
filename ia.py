import requests
import pandas as pd

DATA_FOLDER = "./data/ia/"
ARCHIVE_URL = "http://web.archive.org/"


def get_pdfs(domain):
    params = {
        "url": domain,
        "output": "json",
        "fl": "timestamp, original, length",
        "collapse": "urlkey",
        "filter": "mimetype:application/pdf",
        "matchType": "domain",
        "limit": 150000,
    }

    response = requests.get(ARCHIVE_URL + "cdx/search/cdx", params=params)
    if response.status_code == 200:
        filename = DATA_FOLDER + domain + ".csv"
        data = response.json()
        if not data:
            pd.DataFrame([], columns=["timestamp, original, length"]).to_csv(
                filename, index=False
            )
        else:
            pd.DataFrame(sorted(data[1:]), columns=data[0]).to_csv(
                filename, index=False
            )
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        print(response.text)
