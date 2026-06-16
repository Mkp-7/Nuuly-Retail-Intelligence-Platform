"""
Step 1 — Scrape App Store reviews for the configured app.

Runs automatically via GitHub Actions on every push.
Can also be run locally:
    python module1_voice_of_customer/01_extract_reviews.py

No API key needed. Uses the free iTunes RSS feed.
Outputs: data/reviews.csv
"""

import json
import csv
import os
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    APP_STORE_ID,
    APP_NAME,
    APP_COUNTRY,
    MAX_REVIEW_PAGES,
    DATA_DIR,
    REVIEWS_CSV,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_page(page: int) -> list:
    """Fetch one page of reviews from iTunes RSS feed."""
    url = (
        f"https://itunes.apple.com/{APP_COUNTRY}/rss/customerreviews"
        f"/page={page}/id={APP_STORE_ID}/sortby=mostrecent/json"
    )
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        entries = data.get("feed", {}).get("entry", [])
        # First entry on page 1 is app metadata, not a review
        if page == 1 and entries:
            entries = entries[1:]
        return entries
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []   # No more pages
        print(f"  HTTP {e.code} on page {page} — stopping")
        return []
    except Exception as e:
        print(f"  Error on page {page}: {e}")
        return []


def parse_review(entry: dict) -> dict:
    """Extract fields from a raw iTunes entry dict."""
    return {
        "review_id":  entry.get("id", {}).get("label", ""),
        "stars":      entry.get("im:rating", {}).get("label", ""),
        "date":       entry.get("updated", {}).get("label", "")[:10],
        "title":      entry.get("title", {}).get("label", ""),
        "text":       entry.get("content", {}).get("label", "").replace("\n", " ").strip(),
        "version":    entry.get("im:version", {}).get("label", ""),
        "vote_count": entry.get("im:voteCount", {}).get("label", "0"),
        "app_id":     APP_STORE_ID,
        "app_name":   APP_NAME,
    }


def main():
    print("=" * 55)
    print(f"  Scraping App Store reviews for: {APP_NAME}")
    print(f"  App ID: {APP_STORE_ID} | Country: {APP_COUNTRY}")
    print("=" * 55)

    os.makedirs(DATA_DIR, exist_ok=True)

    all_reviews = []

    for page in range(1, MAX_REVIEW_PAGES + 1):
        print(f"  Fetching page {page}/{MAX_REVIEW_PAGES}...", end=" ")
        entries = fetch_page(page)

        if not entries:
            print("no more pages.")
            break

        reviews = [parse_review(e) for e in entries]
        all_reviews.extend(reviews)
        print(f"got {len(reviews)} reviews (total: {len(all_reviews)})")

        # Be polite — avoid rate limiting
        if page < MAX_REVIEW_PAGES:
            time.sleep(0.5)

    if not all_reviews:
        print("\nNo reviews found. Check APP_STORE_ID in config.py.")
        sys.exit(1)

    # Save to CSV
    fieldnames = ["review_id", "stars", "date", "title", "text", "version", "vote_count", "app_id", "app_name"]
    with open(REVIEWS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_reviews)

    print(f"\n  Saved {len(all_reviews)} reviews → {REVIEWS_CSV}")
    print("=" * 55)
    print("  Done. Run: streamlit run main_app.py")
    print("=" * 55)


if __name__ == "__main__":
    main()
