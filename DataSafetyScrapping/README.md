# Google Play Data Safety Label Collection Pipeline

This component reproduces the Google Play data collection pipeline used in the study.

The pipeline consists of three stages:

1. Collect Google Play Data Safety page URLs.
2. Scrape Data Safety Label disclosures.
3. Extract privacy-policy URLs from Data Safety pages.

## Usage

All commands in this document should be executed from the `DataSafetyScrapping/` directory.

## Installation

Create a Python environment:

```bash
python -m venv venv
```

Activate the environment.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Step 1: Collect Data Safety URLs

Edit:

```text
input/queries.txt
```

and provide one search term per line.

Run:

```bash
python googleplay_collect_urls.py
```

Outputs:

```text
output/ds_urls_by_category.csv
output/Recent_ds_urls.txt
```

## Step 2: Scrape Data Safety Labels

Run:

```bash
python googleplay_scrape_ds.py
```

Output:

```text
output/data_safety_data.json
```

## Step 3: Extract Privacy Policy Links

Run:

```bash
python policyLinkCollection.py
```

Output:

```text
output/privacy_policy_links.txt
```

The output file stores alternating lines:

```text
App Name
Privacy Policy URL
```

## Sample Output

Example Data Safety Label entry:

```json
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
```

## Notes

Google Play may change its page structure over time.

The dataset used for the analyses reported in the paper is already included in the main artifact. Running this pipeline is optional and is not required to reproduce the figures, tables, or quantitative findings reported in the paper.

This component is included to support methodological reproducibility and future extensions of the study.

The included sample queries are intended for lightweight validation of the data-collection workflow.

## Expected Runtime

| Task                       | Runtime                                                                       |
| -------------------------- | ----------------------------------------------------------------------------- |
| Small sample (1–5 queries) | 5–15 minutes                                                                  |
| Full collection            | Several hours, depending on network conditions and Google Play response rates |
