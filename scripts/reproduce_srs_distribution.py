import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

XLSX_PATH = "../data/srs/ppd_ds_comparison_with_verdicts_appscore_1460.xlsx"
SHEET_NAME = "Sensitivity_scores"

RESULTS_DIR = "../results"
FIGURES_DIR = "../figures"

OUTPUT_LOG = os.path.join(RESULTS_DIR, "srs_console_output.txt")
OUTPUT_SUMMARY = os.path.join(RESULTS_DIR, "srs_tier_summary.csv")

OUTPUT_FIGURE = os.path.join(
    FIGURES_DIR,
    "scatter_SRS-Ow_vs_SRS-S_and_SRS-C_unlabeled_and_clustered_2.png"
)

THRESHOLD = 0.70
THRESH_LOW = 0.30
THRESH_HIGH = 0.70



class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()




def risk_tier(x: float) -> str:
    if pd.isna(x):
        return "NA"
    if x < THRESH_LOW:
        return "Low"
    elif x < THRESH_HIGH:
        return "Medium"
    else:
        return "High"


def load_data() -> pd.DataFrame:
    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET_NAME)

    required_cols = ["appname", "SRS-C", "SRS-S", "SRS-O", "SRS-O-weighted"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def compute_srs_summary(df: pd.DataFrame) -> pd.DataFrame:
    total_apps = len(df)

    print(f"Total apps: {total_apps}")

    cols = ["SRS-C", "SRS-S", "SRS-O", "SRS-O-weighted"]

    rows = []

    for col in cols:
        vals = df[col].dropna()

        n_above = (df[col] > THRESHOLD).sum()
        pct_above = n_above / total_apps if total_apps > 0 else 0

        n_low = (vals < THRESH_LOW).sum()
        n_med = ((vals >= THRESH_LOW) & (vals < THRESH_HIGH)).sum()
        n_high = (vals >= THRESH_HIGH).sum()

        pct_low = n_low / total_apps if total_apps > 0 else 0
        pct_med = n_med / total_apps if total_apps > 0 else 0
        pct_high = n_high / total_apps if total_apps > 0 else 0

        print(f"\n{col}:")
        print(f"  {n_above} apps ({pct_above:.2%}) above {THRESHOLD:.0%}")
        print(f"  Low (< {THRESH_LOW:.0%}): {n_low} apps ({pct_low:.2%})")
        print(f"  Medium ({THRESH_LOW:.0%}–{THRESH_HIGH:.0%}): {n_med} apps ({pct_med:.2%})")
        print(f"  High (≥ {THRESH_HIGH:.0%}): {n_high} apps ({pct_high:.2%})")

        rows.append({
            "score": col,
            "n_apps": total_apps,
            "above_0_70_count": n_above,
            "above_0_70_percent": pct_above,
            "low_count": n_low,
            "low_percent": pct_low,
            "medium_count": n_med,
            "medium_percent": pct_med,
            "high_count": n_high,
            "high_percent": pct_high,
        })

    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(OUTPUT_SUMMARY, index=False)

    print(f"\nSaved SRS summary table to: {OUTPUT_SUMMARY}")

    return summary_df


def add_risk_tiers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["risk_tier_overall"] = df["SRS-O-weighted"].apply(risk_tier)
    df["risk_tier_collect"] = df["SRS-C"].apply(risk_tier)
    df["risk_tier_share"] = df["SRS-S"].apply(risk_tier)

    counts = (
        df["risk_tier_overall"]
        .value_counts()
        .reindex(["Low", "Medium", "High"])
        .fillna(0)
        .astype(int)
    )

    print("\nCounts per tier (overall weighted):")
    print(counts)

    print("\nCounts and percentages per tier (overall weighted):")
    for tier in ["Low", "Medium", "High"]:
        c = counts.get(tier, 0)
        p = c / len(df) if len(df) > 0 else 0.0
        print(f"  {tier:6s}: {c} apps ({p:.2%})")

    return df




def plot_figure8(df: pd.DataFrame):
    x_col = "SRS-O-weighted"
    y_cols = [
        ("SRS-S", "Sharing risk score (SRS-S)"),
        ("SRS-C", "Collection risk score (SRS-C)")
    ]

    dfp = df.dropna(subset=[x_col, "SRS-S", "SRS-C"]).copy()

    tier_colors = {
        "Low": "tab:green",
        "Medium": "gold",
        "High": "tab:red"
    }

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True, sharey=True)

    def add_boundaries(ax):
        ax.axvline(THRESH_LOW, linestyle="--", linewidth=2)
        ax.axvline(THRESH_HIGH, linestyle="--", linewidth=2)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    # Top row: unlabeled apps
    for j, (y_col, ylabel) in enumerate(y_cols):
        ax = axes[0, j]
        ax.scatter(dfp[x_col], dfp[y_col], alpha=0.7, s=30)
        add_boundaries(ax)
        ax.set_title("Unlabeled apps")
        ax.set_xlabel("Overall weighted risk score (SRS-O-w)")
        ax.set_ylabel(ylabel)

    # Bottom row: clustered by overall tier
    for j, (y_col, ylabel) in enumerate(y_cols):
        ax = axes[1, j]

        for tier, color in tier_colors.items():
            subset = dfp[dfp["risk_tier_overall"] == tier]
            if subset.empty:
                continue

            ax.scatter(
                subset[x_col],
                subset[y_col],
                alpha=0.7,
                s=30,
                label=tier,
                color=color
            )

        add_boundaries(ax)
        ax.set_title("Clustered by overall weighted tier")
        ax.set_xlabel("Overall weighted risk score (SRS-O-w)")
        ax.set_ylabel(ylabel)

        if j == 0:
            ax.legend(title="Risk tier", loc="upper left")

    plt.tight_layout()
    fig.savefig(OUTPUT_FIGURE, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"\nSaved Figure 8 to: {OUTPUT_FIGURE}")

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    df = load_data()
    compute_srs_summary(df)

    df = add_risk_tiers(df)
    plot_figure8(df)


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(OUTPUT_LOG, "w", encoding="utf-8") as log_file:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log_file)

        try:
            main()
        finally:
            sys.stdout = original_stdout