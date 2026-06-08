# LLM_Privacify

LLM_Privacify is a customized privacy-policy analysis pipeline based on Privacify. The system uses a locally hosted large language model (LLM) through LM Studio to extract structured privacy disclosures from privacy policies.

The pipeline supports extraction of:

* Data collected
* Data shared

## Usage

All commands in this document should be executed from the `LLM_Privacify/` directory.

## Installation and Usage

Detailed setup instructions, LM Studio configuration, input preparation, execution steps, and expected outputs are provided in:

```text
INSTALLATION.md
```

## Main Files

```text
ppaf_scraper.py
requirements.txt
INSTALLATION.md
```

## Input

The pipeline expects a text file containing application names and privacy-policy URLs.

Input location:

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

## Output

Results are written to:

```text
llm_outputs/
```

Each processed application generates a structured JSON output containing extracted privacy disclosures.

Example output:

```json
{
  "collected": [...],
  "shared": [...]
}
```

Depending on the enabled extraction chains, additional fields may be included.

## Notes

The datasets used for the analyses reported in the paper are already included in the main artifact. Running this pipeline is optional and is not required to reproduce the figures, tables, or quantitative findings reported in the paper.

This component is included to support methodological reproducibility and future extensions of the study.

A locally hosted LLM through LM Studio is required to execute the pipeline. No OpenAI API key is required.

## Expected Runtime

Approximate runtime depends on policy length, model configuration, and local hardware.

| Input Size | Runtime       |
| ---------- | ------------- |
| 1 policy   | < 1–2 minutes |
| 5 policies | 5–10 minutes  |

