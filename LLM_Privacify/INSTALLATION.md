# LLM_Privacify Installation and Usage

## Overview

LLM_Privacify is a customized privacy-policy analysis pipeline based on Privacify. The system extracts structured disclosures from privacy policies, including:

* Data collected
* Data shared

The artifact uses a locally hosted LLM through LM Studio and does not require OpenAI API access.

## Usage

All commands in this document should be executed from the `LLM_Privacify/` directory.

---

# Prerequisites

* Python 3.10+
* LM Studio

---

# Step 1: Install LM Studio

Download and install LM Studio:

```text
https://lmstudio.ai/
```

---

# Step 2: Download and Load the Model

Open LM Studio and download:

```text
meta-llama-3.1-8b-instruct
```

Load the model in LM Studio.

Recommended settings:

```text
Context Length: 8500
Server Port: 5000
```

After modifying model settings, unload and reload the model.

---

# Step 3: Start the Local API Server

Open:

```text
Developer → Local Server
```

Enable:

```text
OpenAI-Compatible API Server
```

The server should be available at:

```text
http://127.0.0.1:5000/v1
```

The artifact is configured to use this endpoint.

---

# Step 4: Verify the Server

Run:

```bash
curl http://127.0.0.1:5000/v1/models
```

A successful response should return information about the loaded model.

---

# Step 5: Create Python Environment

From the `LLM_Privacify/` directory:

```bash
conda create -n privacify python=3.10 -y
conda activate privacify
pip install -r requirements.txt
```

---

# Step 6: Prepare Input File

Place the privacy-policy URL list in:

```text
data/input/privacyPolicy_link.txt
```

File format:

```text
App Name
Privacy Policy URL
App Name
Privacy Policy URL
```

Example:

```text
30 Day Fitness Challenge
https://leap.app/privacypolicy.html?pkg=com.popularapp.thirtydayfitnesschallenge
```

Sample input files are included in the artifact.

---

# Step 7: Run the Pipeline

From the `LLM_Privacify/` directory:

```bash
python ppaf_scraper.py
```

---

# Output

Results are written to:

```text
llm_outputs/
```

Each processed application generates a JSON file.

Example:

```json
{
  "collected": [...],
  "shared": [...]
}
```

Depending on the enabled extraction chains, additional fields may be included.

---

# Expected Runtime

Approximate runtime depends on policy length, model configuration, and local hardware.

| Input Size | Runtime              |
| ---------- | -------------------- |
| 1 policy   | Typically < 1 minute |
| 5 policies | 5–10 minutes         |

---
# Hardware Note

The extraction pipeline uses a locally hosted LLM. Runtime varies depending on CPU, GPU, available memory, model quantization, and LM Studio configuration. Systems with dedicated GPUs generally provide significantly faster execution than CPU-only systems.

# Notes

* No OpenAI API key is required.
* LM Studio must be running before executing `ppaf_scraper.py`.
* Sample input files are included in the artifact.
* The datasets used for the analyses reported in the paper are already included in the main artifact. Running this pipeline is optional and is not required to reproduce the figures, tables, or quantitative findings reported in the paper.
* This component is included to support methodological reproducibility and future extensions of the study.
