
import logging
import os
import json
import csv
import functions
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

JSON_PATH = OUTPUT_DIR / "data_safety_data.json"
CSV_PATH = OUTPUT_DIR / "ds_urls_by_category.csv"

# Logging for scraping
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("scraper_progress.log", encoding="utf-8")
    ]
)


def main():
    print("Starting scraping from existing URLs...")

   
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as jf:
                all_apps_data = json.load(jf)
            if not isinstance(all_apps_data, dict):
                logging.warning("Existing JSON is not a dict, starting fresh.")
                all_apps_data = {}
        except Exception as e:
            logging.warning(f"Failed to load existing JSON ({JSON_PATH}): {e}")
            all_apps_data = {}
    else:
        all_apps_data = {}

   
    existing_apps = set(all_apps_data.keys())
    logging.info(f"Loaded {len(existing_apps)} apps from existing JSON")

    try:
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                app_name = row["app_name"]
                ds_url = row["ds_url"]

                if app_name in existing_apps:
                    logging.info(f"Skipping already-scraped app: {app_name}")
                    continue

                logging.info(f"Processing {app_name} → {ds_url}")
                data_safety, scraped_name = functions.scrape_data_safety(ds_url)
                logging.info(f"Finished scraping for {scraped_name}")

                key = scraped_name if scraped_name and scraped_name != "Unknown" else app_name

                all_apps_data[key] = data_safety
                existing_apps.add(key)

    except FileNotFoundError:
        logging.error(f"CSV not found: {CSV_PATH}")
        print(f"CSV not found: {CSV_PATH}")
        return

    functions.save_as_json(all_apps_data, JSON_PATH)
    logging.info(f"Data saved to {JSON_PATH}")
    print(f"Data saved to {JSON_PATH}")


if __name__ == "__main__":
    main()

