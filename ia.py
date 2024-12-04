import time
import requests
from requests.adapters import HTTPAdapter
import pandas as pd

DATA_FOLDER = "./data/ia/"
ARCHIVE_URL = "https://web.archive.org/"
COLUMNS = ["timestamp", "original", "length"]


def save_pdfs(domain, pdfs):
    filename = DATA_FOLDER + domain + ".csv"
    pd.DataFrame(sorted(pdfs), columns=COLUMNS).to_csv(filename, index=False)


def get_pdfs(domain, resume_key=None, previous_page=None):
    if not previous_page:
        previous_page = []

    params = {
        "url": domain,
        "output": "json",
        "fl": "timestamp, original, length",
        "collapse": "urlkey",
        "filter": "mimetype:application/pdf",
        "matchType": "domain",
        "showResumeKey": True,
        "limit": 1000,
    }

    if resume_key:
        params["resumeKey"] = resume_key
        print(f"Resume key: {resume_key}")

    session = requests.Session()
    adapter = HTTPAdapter(max_retries=3)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(ARCHIVE_URL + "cdx/search/cdx", params=params)
    except Exception as e:
        if "Response ended prematurely" in str(e):
            print("Fatal error: saving file...")
            save_pdfs(domain, previous_page)
            return

        print(f"Error: {e}. Waiting 30 seconds...")
        time.sleep(30)
        print("..and retrying now...")
        get_pdfs(domain, resume_key, previous_page)

    if response.status_code == 200:
        data = response.json()

        if not data:
            print("Fetched 0 elements.")
            save_pdfs(domain, [])

        if len(data) > 1 and not data[-2]:
            new_page = data[1:-2]
            resume_key = data[-1][0]
        else:
            new_page = data[1:]
            resume_key = None

        previous_page.extend(new_page)
        print(f"Fetched {len(new_page)} new elements ({len(previous_page)} total).")

        if resume_key:
            get_pdfs(domain, resume_key, previous_page)
        else:
            print(f"No more to fetch, saving {len(previous_page)} elements.")
            save_pdfs(domain, previous_page)
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        print(response.text)
        get_pdfs(domain, resume_key, previous_page)
