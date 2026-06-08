
"""
Reproduce Figure 7: ECDF of cosine similarity between privacy policies
and Data Safety labels, stratified by data operation scope.

"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# CONFIG
INPUT_PATH = "../data/cosinesimilarity/global_label_vs_policy_similarity1460.csv"

RESULTS_DIR = "../results"
FIGURES_DIR = "../figures"

OUTPUT_FIGURE = os.path.join(FIGURES_DIR, "ecdf_cosine_similarity.png")
OUTPUT_LOG = os.path.join(RESULTS_DIR, "cosine_ecdf_console_output.txt")

SCOPES = ["shared", "collected"]


# LOGGING
class Tee:
    """Write console output to both terminal and log file."""
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()



# DATA LOADING
def read_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)

    required_cols = ["app", "section_scope", "cosine_similarity"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["section_scope"] = (
        df["section_scope"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df = df[df["section_scope"].isin(SCOPES)].copy()

    df["cosine_similarity"] = pd.to_numeric(
        df["cosine_similarity"],
        errors="coerce"
    ).clip(0, 1)

    df = df.dropna(subset=["cosine_similarity"])

    return df

# ECDF
def ecdf(values):
    values = np.sort(np.asarray(values))
    y = np.arange(1, len(values) + 1) / len(values)
    return values, y

def save_summary_stats(df: pd.DataFrame):
    rows = []

    for scope in SCOPES:
        vals = df[df["section_scope"] == scope]["cosine_similarity"].dropna()

        if vals.empty:
            continue

        rows.append({
            "section_scope": scope,
            "n": len(vals),
            "mean": vals.mean(),
            "median": vals.median(),
            "min": vals.min(),
            "max": vals.max(),
            "pct_near_zero_le_0_05": (vals <= 0.05).mean(),
            "pct_high_ge_0_80": (vals >= 0.80).mean()
        })

    summary_df = pd.DataFrame(rows)
    output_csv = os.path.join(RESULTS_DIR, "cosine_ecdf_summary.csv")
    summary_df.to_csv(output_csv, index=False)

    print("Cosine similarity summary:")
    print(summary_df)
    print(f"\nSaved summary to: {output_csv}")


def plot_ecdf_by_scope(df):
    plt.figure(figsize=(6,5))

    for scope in SCOPES:
        vals = df[df["section_scope"] == scope]["cosine_similarity"].dropna().values

        if len(vals) == 0:
            continue

        xs, ys = ecdf(vals)
        plt.plot(xs, ys, label=scope)

    plt.xlabel("Cosine similarity")
    plt.ylabel("Proportion of apps ≤ x")
    plt.legend(title="operation scope")
    plt.title("ECDF of cosine similarity by data operation")

    plt.tight_layout()
    plt.savefig(
        OUTPUT_FIGURE,
        dpi=300,
        bbox_inches="tight"
    )
    print(f"\nFigure saved to: {os.path.abspath(OUTPUT_FIGURE)}")
    plt.close()

# MAIN
def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    df = read_data(INPUT_PATH)

    print(f"Loaded input file: {INPUT_PATH}")
    print(df["section_scope"].value_counts())

    save_summary_stats(df)
    plot_ecdf_by_scope(df)


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(OUTPUT_LOG, "w", encoding="utf-8") as log_file:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log_file)

        try:
            main()
        finally:
            sys.stdout = original_stdout