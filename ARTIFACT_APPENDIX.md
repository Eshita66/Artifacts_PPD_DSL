# Artifact Appendix

Paper Title: **Disclosure Divergence: Measuring Privacy Policy and Data Safety Misalignment at Scale**

Requested Badge(s):

* [x] Available
* [x] Functional
* [x] Reproduced

---

# Description

This artifact accompanies the paper:

**Disclosure Divergence: Measuring Privacy Policy and Data Safety Misalignment at Scale**

The artifact contains:

1. A Google Play Data Safety Label (DSL) collection pipeline.
2. A customized LLM-based privacy-policy analysis framework (LLM_Privacify).
3. Processed datasets used in the study.
4. Analysis scripts reproducing the figures, tables, and quantitative findings reported in the paper.

The artifact enables reproduction of the main results reported in Sections 4.1–4.4 as well as the supplementary analyses reported in the appendices.

## Security/Privacy Issues and Ethical Concerns

The artifact does not contain malware, exploits, or intentionally vulnerable software.

The DataSafetyScraping component retrieves publicly available information from Google Play.

The LLM_Privacify component downloads publicly accessible privacy policies and performs automated analysis using a locally hosted language model.

No personally identifiable information (PII) is collected during artifact execution.

No external API keys are required.

---

# Basic Requirements

## Hardware Requirements

Minimum:

* Standard desktop or laptop computer
* 8 GB RAM
* 10 GB available disk space

Recommended:

* 16 GB RAM or greater
* Multi-core CPU

The reproduction scripts do not require a GPU.

For LLM_Privacify, additional memory may improve performance depending on the selected model.

### Hardware Used in Our Experiments

* CPU: Intel Core i9-13900KF
* RAM: 64 GB
* GPU: NVIDIA RTX 4090
* OS: Windows 11

The analysis scripts themselves do not require this hardware configuration.

---

## Software Requirements

Tested Environment:

* Windows 11
* Python 3.11

Required Python dependencies are listed in:

```text
requirements.txt
```

The privacy-policy extraction component additionally requires:

* LM Studio
* meta-llama-3.1-8b-instruct

Recommended LM Studio settings:

```text
Context Length: 8500
Server Port: 5000
```

The local API endpoint should be:

```text
http://127.0.0.1:5000/v1
```

---

## Estimated Time and Storage Consumption

Artifact size:

* Approximately XX GB

Approximate runtimes:

| Task              | Runtime      |
| ----------------- | ------------ |
| RQ1 reproduction  | 2–5 minutes  |
| RQ2 reproduction  | < 2 minutes  |
| RQ3 reproduction  | < 1 minute   |
| RQ4 reproduction  | < 1 minute   |
| Appendix analyses | < 1 minute   |
| Full reproduction | 5–15 minutes |

Data collection pipelines require additional time depending on network conditions.

---

# Environment

## Accessibility

The artifact is available through the project repository:

```text
https://github.com/Eshita66/Artifacts_PPD_DSL
```

A stable release tag corresponding to the evaluated artifact will be maintained.

---

## Set Up the Environment

Clone the repository:

```bash
git clone <repository_url>
cd Artifacts_PPD_DSL
```

Create a virtual environment:

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

## Testing the Environment

Run:

```bash
python scripts/reproduce_prevalence.py
```

Successful execution should generate output files in:

```text
figures/
results/
```

This confirms that the analysis environment has been configured correctly.

---

# Evaluation and Expected Results

## Experiment 1: Consistency Analysis (RQ1)

### Figure 2

Run:

```bash
python scripts/reproduce_prevalence.py
```

Expected output:

```text
figures/overall_agreement_vs_misalignment.png
```

Expected statistics:

| Operation  | Agreement Rate |
| ---------- | -------------- |
| Collection | 66.87%         |
| Sharing    | 68.93%         |

Expected misaligned cells:

| Operation  | Misaligned Cells |
| ---------- | ---------------- |
| Collection | 28,066           |
| Sharing    | 26,322           |

### Figure 3

Run:

```bash
python scripts/reproduce_kappaScore.py
```

Expected output:

```text
figures/violin_kappa_distribution.png
```

The generated distribution should visually match Figure 3 in the paper.

---

## Experiment 2: Category-Level and Semantic Consistency Analysis (RQ2)

### Figures 4–6

Run:

```bash
python scripts/reproduce_prevalence.py
```

Expected outputs:

```text
figures/category_level_misalignment.png
figures/data_safety_only_misalignment.png
figures/privacy_policy_only_misalignment.png
```

### Figure 7

Generate cosine similarity data:

```bash
python scripts/generate_cosine_similarity_dataset.py
```

Generate ECDF visualization:

```bash
python scripts/reproduce_cosine_ecdf.py
```

Expected output:

```text
figures/ecdf_cosine_similarity.png
```

The ECDF curves should visually match Figure 7.

---

## Experiment 3: Sensitivity Risk Score Analysis (RQ3)

Run:

```bash
python scripts/reproduce_srs_distribution.py
```

Expected output:

```text
figures/scatter_SRS-Ow_vs_SRS-S_and_SRS-C_unlabeled_and_clustered_2.png
```

The resulting visualization should visually match Figure 8.

---

## Experiment 4: App Category-Level Risk Analysis (RQ4)

Run:

```bash
python scripts/reproduce_category_risk_and_popularity.py
```

Expected outputs:

```text
figures/mean_SRS_by_category_top20.png
figures/risk_tier_distribution_by_category_top20.png
```

These correspond to Figures 9 and 10.

Appendix E outputs:

```text
figures/rating_vs_SRS-O-weighted.png
figures/downloads_vs_SRS-O-weighted_log10.png
```

Expected correlation matrix:

```text
                SRS-O-weighted  rating  reviews_num  downloads_num
SRS-O-weighted           1.000  -0.001        0.034          0.072
rating                  -0.001   1.000        0.034          0.075
reviews_num              0.034   0.034        1.000          0.667
downloads_num            0.072   0.075        0.667          1.000
```

---

## Experiment 5: Appendix Robustness Analyses

### Alpha Sensitivity Analysis

Run:

```bash
python scripts/reproduce_alpha_sensitivity.py
```

Expected outputs:

```text
results/alpha_sensitivity_results.xlsx
results/alpha_sensitivity_summary.csv
```

The resulting table should match the appendix sensitivity analysis.

### Generic Sharing Statement Analysis

Run:

```bash
python scripts/reproduce_generic_sharing_ablation.py
```

Expected output:

```text
results/generic_sharing_analysis.csv
```

The resulting statistics should match the appendix robustness analysis.

---

# Notes


The DataSafetyScraping and LLM_Privacify components are included to support methodological reproducibility and future research.
