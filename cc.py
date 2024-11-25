import os
import time
import json
import requests
from downloader import Downloader

CC_URL = "https://index.commoncrawl.org"
LIST_URL = CC_URL + "/collinfo.json"


def get_collinfo():
    path = "collinfo.json"
    if os.path.exists(path):
        with open(path, "r") as file:
            return json.load(file)

    return requests.get(LIST_URL).json()


def get_pdf_links(downloader: Downloader, cdx_api, url):
    params = {
        "url": url,
        "output": "json",
        "matchType": "domain",
        "filter": "mime:pdf",
        "fl": "url",
    }

    try:
        response = requests.get(cdx_api, params=params)
        # response = downloader.fetch(cdx_api, params)
    except ConnectionError as e:
        print("Sleeping before retry...")
        time.sleep(2)
        return get_pdf_links(downloader, cdx_api, url)
    except requests.exceptions.ConnectionError:
        print("Connection aborted")
        exit()

    if response.status_code == 404:
        return []
    elif response.status_code != 200:
        print("Sleeping before retry...")
        time.sleep(2)
        return get_pdf_links(downloader, cdx_api, url)

    json_lines = response.text.splitlines()

    return [json.loads(line) for line in json_lines]
