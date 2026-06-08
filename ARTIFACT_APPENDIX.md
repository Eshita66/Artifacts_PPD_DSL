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
3. Datasets used in the study.
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

* Approximately 686 MB

Approximate runtimes:

| Task              | Runtime      |
| ----------------- | ------------ |
| RQ1 reproduction  | 1-3 minutes  |
| RQ2 reproduction  | < 1 minute   |
| RQ3 reproduction  | < 1 minute   |
| RQ4 reproduction  | < 1 minute   |
| Appendix analyses | < 1 minute   |
| Full reproduction | 5–8 minutes  |

Data collection pipelines may require additional time depending on hardware configuration, local LLM settings, and network conditions.

---

# Environment

## Accessibility

The artifact is available through the project repository:

```text
https://github.com/Eshita66/Artifacts_PPD_DSL
```

---

## Set Up the Environment

Clone the repository:

```bash
git clone https://github.com/Eshita66/Artifacts_PPD_DSL
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

After installing the required dependencies, navigate to the `scripts` directory:

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

Expected console output should report approximately:

```text
Kappa (collection): 0.318
Kappa (sharing): 0.167
```

This confirms that the analysis environment has been configured correctly.

# Evaluation and Expected Results

The following experiments reproduce the figures, tables, and quantitative findings reported in the paper. Unless otherwise specified, commands should be executed from the `scripts/` directory.

## Experiment 1: Consistency Analysis (RQ1)

### Figure 2: Overall Agreement and Misalignment Rates

Run:

```bash
python reproduce_prevalence.py
```

Expected output:

```text
../figures/overall_consistency.png
```

Expected Figure 2 statistics:

| Operation  | Agreement (PPD = DSL) | Misalignment in DSL Only | Misalignment in PPD Only |
| ---------- | --------------------- | ------------------------ | ------------------------ |
| Collection | ≈ 66.9%               | ≈ 23.7%                  | ≈ 9.5%                   |
| Sharing    | ≈ 68.9%               | ≈ 26.0%                  | ≈ 5.0%                   |


### Figure 3: Cohen's κ Analysis

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

Expected overall κ values:

| Operation  | Cohen's κ |
| ---------- | --------- |
| Collection | ≈ 0.318   |
| Sharing    | ≈ 0.167   |

---

## Experiment 2: Data Category-Level and Semantic Consistency Analysis (RQ2)

### Figures 4–6: Data Category-Level Misalignment Analysis

Run:

```bash
python reproduce_prevalence.py
```

Expected outputs:

```text
../figures/misalignment_heatmap.png
../figures/category_level_under.png
../figures/category_level_over.png
```

Expected category-level misalignment values include:
- Personal info (sharing): ≈72.0%
- Device or other IDs (sharing): ≈55.1%
- Photos and videos (collection): ≈51.6%
- Location (collection): ≈51.1%


### Figure 7: Semantic Consistency Analysis

Generate the cosine similarity dataset:

```bash
python generate_cosine_similarity_dataset.py
```

Then generate the ECDF visualization:

```bash
python reproduce_cosine_ecdf.py
```

Expected outputs:

```text
../figures/ecdf_cosine_similarity.png
../results/cosine_ecdf_summary.csv
```

Expected cosine similarity summary:

| Scope     | Mean    | Median  |
| --------- | ------- | ------- |
| Shared    | ≈ 0.183 | ≈ 0.000 |
| Collected | ≈ 0.461 | ≈ 0.479 |

---

## Experiment 3: Sensitivity Risk Score Analysis (RQ3)

### Figure 8: Sensitivity Risk Score Distribution

Run:

```bash
python reproduce_srs_distribution.py
```

Expected outputs:

```text
../figures/scatter_SRS-Ow_vs_SRS-S_and_SRS-C_unlabeled_and_clustered_2.png
../results/srs_tier_summary.csv
```

Expected overall weighted risk-tier distribution:

| Tier   | Apps | Percentage |
| ------ | ---- | ---------- |
| Low    | 3002 | 49.61%     |
| Medium | 2971 | 49.10%     |
| High   | 78   | 1.29%      |


---

## Experiment 4: App Category-Level Risk Analysis (RQ4)

### Figures 9 and 10: App Category-Level Risk Analysis

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

The generated outputs reproduce:

* Figure 9: Risk scores across app categories.
* Figure 10: Distribution of app categories across risk tiers.

### Appendix E: Additional Quantitative Analysis (RQ5)

Run:

```bash
python reproduce_category_risk_and_popularity.py
```

Expected outputs:

```text
../figures/rating_vs_SRS-O-weighted.png
../figures/downloads_vs_SRS-O-weighted_log10.png
../results/srs_popularity_correlation_matrix.csv
```

These outputs reproduce:

* Figure 12: Rating vs Risk Score.
* Figure 13: Downloads vs Risk Score.

The generated visualizations examine the relationship between privacy misalignment risk and application popularity metrics, including user ratings and download counts.

## Experiment 5: Alpha Sensitivity Analysis (Appendix H)

### Table 5: Sensitivity Analysis of Risk-Tier Distribution Under Alternative α Values

Run:

```bash
python reproduce_alpha_sensitivity.py
```

Expected outputs:

```text
../results/alpha_sensitivity_results.xlsx
../results/alpha_sensitivity_summary.csv
```

Expected Table 5 values:

| α   | Low (%) | Medium (%) | High (%) | Same Tier (%) |
| --- | ------- | ---------- | -------- | ------------- |
| 0.4 | 46.84   | 51.96      | 1.21     | 90.56         |
| 0.5 | 49.96   | 48.83      | 1.21     | 96.00         |
| 0.6 | 49.61   | 49.10      | 1.29     | 100.00        |
| 0.7 | 51.02   | 47.61      | 1.37     | 96.20         |

The resulting outputs should reproduce the alpha sensitivity analysis reported in Table 5 and demonstrate that the SRS-based risk stratification remains stable under alternative α parameter settings.

---

# Notes

The DataSafetyScrapping and LLM_Privacify components are included to support methodological reproducibility and future research. The datasets required to reproduce all figures, tables, and quantitative findings reported in the paper are already included in the artifact. Running these pipelines is optional and is not required for reproducing the published results.

## Optional Pipeline Validation

The artifact also includes the original data collection and privacy-policy analysis pipelines used to construct the datasets analyzed in the paper.

### DataSafetyScrapping

The DataSafetyScrapping component collects:

* Google Play Data Safety Labels
* Privacy Policy URLs

Detailed setup, configuration, and execution instructions are provided in:

```text
DataSafetyScrapping/README.md
```

### LLM_Privacify

The LLM_Privacify component reproduces the privacy-policy analysis pipeline used in the study, including privacy-policy retrieval, preprocessing, disclosure extraction, and structured output generation.

Detailed setup, LM Studio configuration, and execution instructions are provided in:

```text
LLM_Privacify/README.md
```

Execution of these pipelines is optional and is not required for reproducing the figures, tables, and quantitative findings reported in the paper.
