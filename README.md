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
├── DataSafetyScraping/
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

---

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

This confirms that the environment has been configured correctly.

---

# Reproducing Paper Results

## Claim 1: Consistency Between Privacy Policies and Data Safety Labels (RQ1)

RQ1 is reproduced using two scripts.

### Step 1: Reproduce overall agreement and misalignment rates

This generates Figure 2.

```bash
python reproduce_prevalence.py
```
Expected Outputs:
figures/overall_agreement_vs_misalignment.png

The script also prints agreement and misalignment rates for collection and sharing.
### Step 2: Reproduce Cohen's κ analysis

This generates Figure 3.

```bash
python reproduce_kappaScore.py
```
Expected Output:
figures//kappa_violin_by_operation.png

---

## Claim 2: Category-Level Misalignment Analysis (RQ2)

# Part A: Category-Level Misalignment Analysis
Reproduces Figure 4, Figure 5, and Figure 6.

Run:

```bash
python reproduce_prevalence.py
```

Expected outputs:
figures/category_level_misalignment.png
figures/data_safety_only_misalignment.png
figures/privacy_policy_only_misalignment.png

---

# Part B: Semantic Consistency Analysis

### Step 1: Generate cosine similarity dataset

```bash
python generate_cosine_similarity_dataset.py
```

Output:

```text
data/cosinesimilarity/global_label_vs_policy_similarity1460.csv
```

### Step 2: Generate Figure 7

```bash
python reproduce_cosine_ecdf.py
```

Output:

```text
figures/ecdf_cosine_similarity.png
```
---

## Claim 3: Sensitivity Risk Score Analysis (RQ3)

Reproduces Figure 8.

Run:

```bash
python reproduce_srs_distribution.py
```

Output:

```text
figures/scatter_SRS-Ow_vs_SRS-S_and_SRS-C_unlabeled_and_clustered_2.png
```
The script computes:

* SRS-C (collection risk)
* SRS-S (sharing risk)
* SRS-O-w (overall weighted risk)
* Risk-tier distributions

---

## Claim 4: App Category-Level Risk Analysis (RQ4)

Reproduces Figure 9 and Figure 10.

Run:

```bash
python reproduce_category_risk_and_popularity.py
```

Outputs:

```text
figures/mean_SRS_by_category_top20.png
figures/risk_tier_distribution_by_category_top20.png
```
In addition, this script reproduces the popularity-based analyses reported in the appendix E, including:

figures/rating_vs_SRS-O-weighted.png
figures/downloads_vs_SRS-O-weighted_log10.png

and the associated correlation statistics between privacy risk and application popularity metrics.


## Claim 5: Robustness of SRS-based risk stratification (Appendix H) 

Sensitivity analysis of risk-tier distribution under alternative 𝛼 values

Run:

```bash
python reproduce_alpha_sensitivity.py

```
Expected outputs:

results/alpha_sensitivity_results.xlsx
results/alpha_sensitivity_summary.csv

This reproduces the alpha-sensitivity analysis reported in the appendix H and verifies that the overall conclusions remain stable across different settings.

# Data Collection Pipelines

## DataSafetyScraping

The DataSafetyScraping component reproduces the collection of:

* Google Play Data Safety Labels
* Privacy Policy URLs

See:

```
DataSafetyScraping/README.md for detailed instructions.

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

See:

```text
LLM_Privacify/README.md for LM Studio configuration and execution instructions.
```


---

# Expected Runtime

Approximate runtime on a standard desktop machine:

| Task                      | Runtime  |
| ------------------------- | -------- |
| RQ1–RQ2 reproduction      | 2–5 min  |
| RQ3 reproduction          | <1 min   |
| RQ4 reproduction          | <1 min   |
| Full results reproduction | 5–10 min |

Data collection pipelines require additional time depending on network conditions.

---

