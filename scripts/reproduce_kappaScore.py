
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score

EXCEL_PATH = "../data/kappa/ppd_ds_comparison_with_verdicts_1460.xlsx"
SHEET_NAME = "Verdicts"

RESULTS_DIR = "../results"
FIGURES_DIR = "../figures"

OUTPUT_CATEGORY_KAPPA_XLSX = os.path.join(RESULTS_DIR, "kappa_by_category.xlsx")
OUTPUT_OVERALL_KAPPA_CSV = os.path.join(RESULTS_DIR, "overall_kappa.csv")
OUTPUT_FIGURE = os.path.join(FIGURES_DIR, "kappa_violin_by_operation.png")
OUTPUT_LOG = os.path.join(RESULTS_DIR, "kappa_console_output.txt")


class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()


def load_verdicts() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

    required_cols = ["Operation", "Category", "PPD", "DS"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=["PPD", "DS"])
    df["PPD"] = df["PPD"].astype(int)
    df["DS"] = df["DS"].astype(int)

    return df


def compute_overall_kappa(df: pd.DataFrame):
    df_collect = df[df["Operation"] == "collected"].copy()
    df_share = df[df["Operation"] == "shared"].copy()

    kappa_collect = cohen_kappa_score(df_collect["PPD"], df_collect["DS"])
    kappa_share = cohen_kappa_score(df_share["PPD"], df_share["DS"])

    return kappa_collect, kappa_share


def kappa_by_category(df: pd.DataFrame, op_label: str) -> pd.DataFrame:
    df_op = df[df["Operation"] == op_label].copy()

    rows = []

    for cat, g in df_op.groupby("Category"):
        if g["PPD"].nunique() == 1 and g["DS"].nunique() == 1:
            kappa = np.nan
        else:
            kappa = cohen_kappa_score(g["PPD"], g["DS"])

        rows.append({
            "Operation": op_label,
            "Category": cat,
            "N": len(g),
            "Kappa": kappa
        })

    return pd.DataFrame(rows).sort_values(
        ["Kappa", "Category"],
        ascending=[True, True]
    ).reset_index(drop=True)


def bootstrap_kappa_for_violin(df: pd.DataFrame, B: int = 1000, random_state: int = 42):
    rng = np.random.default_rng(random_state)

    df_collect = df[df["Operation"] == "collected"].reset_index(drop=True)
    df_share = df[df["Operation"] == "shared"].reset_index(drop=True)

    k_collect_samples = []
    k_share_samples = []

    for _ in range(B):
        sample_collect = df_collect.loc[
            rng.integers(0, len(df_collect), len(df_collect))
        ]
        sample_share = df_share.loc[
            rng.integers(0, len(df_share), len(df_share))
        ]

        k_collect_samples.append(
            cohen_kappa_score(sample_collect["PPD"], sample_collect["DS"])
        )
        k_share_samples.append(
            cohen_kappa_score(sample_share["PPD"], sample_share["DS"])
        )

    return np.array(k_collect_samples), np.array(k_share_samples)


def make_kappa_violinplot(df: pd.DataFrame):
    k_collect_samples, k_share_samples = bootstrap_kappa_for_violin(df)

    data = [k_share_samples, k_collect_samples]
    labels = ["shared", "collected"]
    positions = np.arange(1, 3)

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.violinplot(
        data,
        positions=positions,
        showmeans=True,
        showmedians=True,
        showextrema=True
    )

    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Data Operation")
    ax.set_ylabel("Cohen's Kappa")
    ax.set_title("PPD Vs. DSL Cohen's Kappa by data operation")
    ax.set_ylim(0.00, 0.40)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    fig.savefig(OUTPUT_FIGURE, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved Kappa violin plot to: {OUTPUT_FIGURE}")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    df = load_verdicts()

    kappa_collect, kappa_share = compute_overall_kappa(df)

    print("=== Overall Kappa by Operation ===")
    print(f"Kappa (collection): {kappa_collect:.3f}")
    print(f"Kappa (sharing):   {kappa_share:.3f}")
    print(f"Difference (sharing - collection): {kappa_share - kappa_collect:.3f}")
    print()

    overall_df = pd.DataFrame({
        "Operation": ["collection", "sharing"],
        "Kappa": [kappa_collect, kappa_share]
    })
    overall_df.to_csv(OUTPUT_OVERALL_KAPPA_CSV, index=False)
    print(f"Saved overall Kappa table to: {OUTPUT_OVERALL_KAPPA_CSV}")

    df_kappa_collect = kappa_by_category(df, op_label="collected")
    df_kappa_share = kappa_by_category(df, op_label="shared")

    df_kappa_all = pd.concat(
        [df_kappa_collect, df_kappa_share],
        ignore_index=True
    )

    df_kappa_all.to_excel(OUTPUT_CATEGORY_KAPPA_XLSX, index=False)
    print(f"Saved category-level Kappa table to: {OUTPUT_CATEGORY_KAPPA_XLSX}")

    make_kappa_violinplot(df)


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(OUTPUT_LOG, "w", encoding="utf-8") as log_file:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log_file)

        try:
            main()
        finally:
            sys.stdout = original_stdout