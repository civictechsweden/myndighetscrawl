import os
import time
import json
import requests

LIST_URL = "https://index.commoncrawl.org/collinfo.json"


def get_collinfo():
    path = "collinfo.json"
    if os.path.exists(path):
        with open(path, "r") as file:
            return json.load(file)

    return requests.get(LIST_URL).json()


def get_pdf_links(cdx_api, url):
    params = {
        "url": url,
        "output": "json",
        "matchType": "domain",
        "filter": "mime:pdf",
        "fl": "url",
    }

    response = requests.get(cdx_api, params=params)

    if response.status_code == 404:
        return []
    elif response.status_code != 200:
        print("Sleeping before retry...")
        time.sleep(2)
        return get_pdf_links(cdx_api, url)

    json_lines = response.text.splitlines()

    return [json.loads(line) for line in json_lines]
