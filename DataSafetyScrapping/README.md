### Google Play Data Safety Label Collection Pipeline

The pipeline consists of three steps:
Collect Data Safety URLs from Google Play.
Scrape Data Safety Label disclosures.
Extract privacy-policy links from Data Safety pages.

# Installation

Create a Python environment:

python -m venv venv
source venv/bin/activate

# Install dependencies:

pip install -r requirements.txt


### Step 1: Collect Data Safety URLs

Edit:
input/queries.txt and provide one search term per line.

Run:

python googleplay_collect_urls.py

Output:

output/ds_urls_by_category.csv
output/Recent_ds_urls.txt

### Step 2: Scrape Data Safety Labels

Run:

python googleplay_scrape_ds.py

Output:

output/data_safety_data.json

### Step 3: Extract Privacy Policy Links

Run:

python policyLinkCollection.py

Output:

output/privacy_policy_links.txt

The output file stores alternating lines:

App Name
Privacy Policy URL

Sample Output: 
Example DSL entry:

{
  "Data shared": {
    "Location": "...",
    "Personal info": "..."
  },
  "Data collected": {
    "App activity": "...",
    "Device or other IDs": "..."
  }
}
# Notes
Google Play may change page structure over time.
Full reproduction of the original dataset may take several hours.
The processed dataset used in the paper is included separately in the artifact.
This scraper is provided to reproduce the data-collection process on a small sample.

The included sample queries are intended for functional verification.
## Expected Runtime

Small sample (1–5 queries):
5–15 minutes

Full collection:
Several hours depending on network conditions and Google Play response rates.

## Reproducibility Notes

The artifact includes:

- The DSL scraping pipeline.
- The privacy-policy link collection pipeline.

