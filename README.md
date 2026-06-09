# Disclosure Divergence: Measuring Privacy Policy and Data Safety Misalignment at Scale

## Artifact Overview

**Disclosure Divergence: Measuring Privacy Policy and Data Safety Misalignment at Scale**

The artifact provides:

1. **Data Safety Label Collection Pipeline** for collecting Google Play Data Safety disclosures and privacy-policy URLs.
2. **LLM-Based Privacy Policy Analysis Pipeline** based on a customized version of Privacify for extracting data collection and sharing disclosures from privacy policies.
3. **Datasets** used in the study.
4. **Analysis Scripts** reproducing the figures, tables, and quantitative findings reported in the paper.

The artifact supports reproduction of the results presented in Sections 4.1–4.4 and the supplementary analyses reported in the appendices.

---

# Repository Structure

```text
Artifacts_PPD_DSL/
│
├── README.md
├── ARTIFACT_APPENDIX.md
├── requirements.txt
│
├── data/
│
├── scripts/
│   ├── reproduce_prevalence.py
│   ├── reproduce_kappaScore.py
│   ├── generate_cosine_similarity_dataset.py
│   ├── reproduce_cosine_ecdf.py
│   ├── reproduce_srs_distribution.py
│   ├── reproduce_category_risk_and_popularity.py
│   └── reproduce_alpha_sensitivity.py
│
├── DataSafetyScrapping/
│
├── LLM_Privacify/
│
├── figures/
├── results/

```

---

# Installation

Create a Python virtual environment:

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

Note: The root requirements.txt installs all dependencies required for the artifact. Component-specific requirements.txt files are provided for standalone use of DataSafetyScrapping and LLM_Privacify.

# Environment Verification
After installing the required dependencies, navigate to the scripts directory:
```bash
cd scripts
```
Run:
```bash
python reproduce_kappaScore.py
```

Successful execution should:
1. Complete without errors.
2. Print the overall Cohen's κ values for collection and sharing disclosures.
3. Generate the following files:
```text
../results/overall_kappa.csv
../results/kappa_by_category.xlsx
../figures/kappa_violin_by_operation.png
```
This confirms that the environment has been configured correctly.

---

# Reproducing Paper Results

## Claim 1: Consistency Between Privacy Policies and Data Safety Labels (RQ1)

RQ1 is reproduced using two scripts.

### Step 1: Reproduce overall agreement and misalignment rates

This generates Figure 2.

Run:

```bash
python reproduce_prevalence.py
```
Expected outputs:
```text
../figures/overall_consistency.png
```
In addition to Figure 2, the script reports:
- Data category-level misalignment rates
- Misalignment rates attributable to Data Safety Labels only
- Misalignment rates attributable to Privacy Policies only
  
### Step 2: Reproduce Cohen's κ analysis

This generates Figure 3.
Run:

```bash
python reproduce_kappaScore.py
```

Expected outputs:
```text
../figures/kappa_violin_by_operation.png
../results/overall_kappa.csv
../results/kappa_by_category.xlsx
```
The script computes Cohen's κ scores for collection and sharing disclosures and generates the summary and visualization reported in Figure 3.


## Claim 2: Data Category-Level Misalignment Analysis (RQ2)

### Part A: Data Category-Level Misalignment Analysis
Reproduces Figures 4–6.
The same script used for RQ1 also computes the category-level misalignment analyses reported in Figures 4–6.
Run:

```bash
python reproduce_prevalence.py
```

Expected outputs:
```text
../figures/overall_consistency.png
../figures/misalignment_heatmap.png
../figures/category_level_under.png
../figures/category_level_over.png
```
In addition to generating these figures, the script reports:
- Data category-level misalignment rates
- Misalignment rates attributable to Data Safety Labels only
- Misalignment rates attributable to Privacy Policies only
- App-level misalignment prevalence
---

### Part B: Semantic Consistency Analysis

### Step 1: Generate cosine similarity dataset
Run:

```bash
python generate_cosine_similarity_dataset.py
```
Expected output:
```text
../data/cosinesimilarity/global_label_vs_policy_similarity1460.csv
```
This script computes cosine similarity scores between Privacy Policy and Data Safety Label disclosures and generates the dataset used for semantic consistency analysis.
### Step 2: Generate the ECDF of Cosine Similarity
Reproduces Figure 7.
Run:

```bash
python reproduce_cosine_ecdf.py
```
Expected outputs:
```text
../figures/ecdf_cosine_similarity.png
../results/cosine_ecdf_summary.csv
```
The script generates the ECDF visualization and summary statistics reported in Figure 7.

## Claim 3: Sensitivity Risk Score Analysis (RQ3)

Reproduces Figure 8.
Run:
```bash
python reproduce_srs_distribution.py
```

Expected outputs:
```text
../figures/scatter_SRS-Ow_vs_SRS-S_and_SRS-C_unlabeled_and_clustered_2.png
../results/srs_tier_summary.csv
```
The script computes:
- SRS-C (collection risk)
- SRS-S (sharing risk)
- SRS-O (overall risk)
- SRS-O-w (overall weighted risk)
- Risk-tier distributions

---

## Claim 4: App Category-Level Risk Analysis (RQ4)

Reproduces Figures 9 and 10.
Run:

```bash
python reproduce_category_risk_and_popularity.py
```
Expected outputs:
```text
../figures/mean_SRS_by_category_top20.png
../figures/risk_tier_distribution_by_category_top20.png
../results/category_srs_stats.csv
../results/risk_tier_distribution_by_category_top20.csv
```
The script computes application category-level privacy misalignment risk statistics, identifies the app categories with the highest privacy misalignment risk, and examines how risk is distributed across low-, medium-, and high-risk tiers within each category.

### Additional Quantitative Analysis (Appendix E)

The same script used for RQ4 also reproduces the popularity-based analyses reported in Appendix E (Figures 12 and 13).

Additional outputs:

```text
../figures/rating_vs_SRS-O-weighted.png
../figures/downloads_vs_SRS-O-weighted_log10.png
../results/srs_popularity_correlation_matrix.csv
```
These outputs examine the relationship between privacy misalignment risk and application popularity metrics, including user ratings, review counts, and download counts.


## Appendix H: Alpha Sensitivity Analysis

Reproduces Table 5.

Run:

```bash
python reproduce_alpha_sensitivity.py
```
Expected outputs:
```text
../results/alpha_sensitivity_results.xlsx
../results/alpha_sensitivity_summary.csv
```
This reproduces the sensitivity analysis reported in Table 5 and evaluates the robustness of the SRS-based risk stratification under alternative α parameter settings.

# Data Collection Pipelines
Note: The processed datasets required to reproduce all figures, tables, and quantitative findings reported in the paper are already included in the artifact. Running the DataSafetyScrapping and LLM_Privacify pipelines is optional and is not required for reproducing the published results.

## DataSafetyScrapping

The DataSafetyScrapping component reproduces the collection of:

- Google Play Data Safety Labels
- Privacy Policy URLs

Detailed setup and execution instructions are provided in:

```text
DataSafetyScrapping/README.md
```
---

## LLM_Privacify

The LLM_Privacify component reproduces privacy-policy analysis using a local LLM backend.

The pipeline:

1. Downloads privacy policies.
2. Chunks and preprocesses policy text.
3. Extracts data collection disclosures.
4. Extracts data sharing disclosures.
5. Produces structured JSON outputs.

Detailed setup and execution instructions are provided in:
```text
LLM_Privacify/README.md
```

---

# Expected Runtime

Approximate runtime on a standard desktop machine:

| Task                      | Runtime  |
| ------------------------- | -------- |
| RQ1–RQ2 reproduction      | 1–3 min  |
| RQ3 reproduction          | <1 min   |
| RQ4 reproduction          | <1 min   |
| Full results reproduction | 5–7 min |

Data collection pipelines may require additional time depending on hardware configuration, local LLM settings, and network conditions.

---

