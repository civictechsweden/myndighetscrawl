# Myndighetscrawl

Myndighetscrawl is an attempt at extracting Swedish government agency information from CommonCrawl. More specifically, it iterates through these agencies' domain names and looks for PDF document links from these domains in the CommonCrawl index.

Since the index contains links fetched over 10 years ago, they are not all valid.

# Set up

```bash
pip install -r requirements.txt
```

# Usage

```bash
python run.py
```
