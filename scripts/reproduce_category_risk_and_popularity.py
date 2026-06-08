import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

XLSX_PATH = "../data/srs/ppd_ds_comparison_with_verdicts_appscore_1460_metadata.xlsx"
SHEET_NAME = "Sensitivity_scores_with_meta"

RESULTS_DIR = "../results"
FIGURES_DIR = "../figures"

OUTPUT_LOG = os.path.join(RESULTS_DIR, "category_risk_console_output.txt")

FIG_MEAN_SRS_CATEGORY = os.path.join(FIGURES_DIR, "mean_SRS_by_category_top20.png")
FIG_RISK_TIER_CATEGORY = os.path.join(FIGURES_DIR, "risk_tier_distribution_by_category_top20.png")
FIG_RATING_RISK = os.path.join(FIGURES_DIR, "rating_vs_SRS-O-weighted.png")
FIG_DOWNLOADS_RISK = os.path.join(FIGURES_DIR, "downloads_vs_SRS-O-weighted_log10.png")

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


def parse_km(val):
    """
    Parse strings like '50.7K', '10M+', '1,234', '500K+' into numeric counts.
    Returns float or NaN.
    """
    if isinstance(val, str):
        s = val.strip().replace("+", "")
        s = s.replace(",", "")

        if s.endswith("K"):
            try:
                return float(s[:-1]) * 1_000
            except ValueError:
                return np.nan

        if s.endswith("M"):
            try:
                return float(s[:-1]) * 1_000_000
            except ValueError:
                return np.nan

        try:
            return float(s)
        except ValueError:
            return np.nan

    return np.nan


def load_data():
    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET_NAME)

    required_cols = ["Category", "SRS-O-weighted"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=["Category", "SRS-O-weighted"]).copy()
    return df


def reproduce_rq4_category_risk(df):
    cat_stats = (
        df.groupby("Category")["SRS-O-weighted"]
        .agg(["count", "mean", "median", "std"])
        .sort_values("mean", ascending=False)
    )

    cat_stats_path = os.path.join(RESULTS_DIR, "category_srs_stats.csv")
    cat_stats.to_csv(cat_stats_path)

    print("Category-level stats (SRS-O-weighted):")
    print(cat_stats)
    print(f"\nSaved category stats to: {cat_stats_path}")

    cat_stats_top20 = cat_stats.head(20)
    top_categories = cat_stats_top20.index.tolist()

    # Figure 
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(range(len(cat_stats_top20.index)), cat_stats_top20["mean"])

    ax.set_ylabel("Mean SRS-O-weighted")
    ax.set_xlabel("App category")
    ax.set_title("Mean Sensitivity Risk Score by App Category (Top 20)")
    ax.set_xticks(range(len(cat_stats_top20.index)))
    ax.set_xticklabels(cat_stats_top20.index, rotation=45, ha="right")

    plt.tight_layout()
    fig.savefig(FIG_MEAN_SRS_CATEGORY, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved Figure to: {FIG_MEAN_SRS_CATEGORY}")

    # Figure 
    df = df.copy()
    df["risk_tier_overall"] = df["SRS-O-weighted"].apply(risk_tier)

    df_top = df[df["Category"].isin(top_categories)]

    ctab = pd.crosstab(df_top["Category"], df_top["risk_tier_overall"])

    for tier in ["Low", "Medium", "High"]:
        if tier not in ctab.columns:
            ctab[tier] = 0

    ctab = ctab[["Low", "Medium", "High"]]
    ctab_pct = ctab.div(ctab.sum(axis=1), axis=0)

    ctab_path = os.path.join(RESULTS_DIR, "risk_tier_distribution_by_category_top20.csv")
    ctab_pct.to_csv(ctab_path)

    print("\nRisk tier distribution by category (proportions, top 20 categories):")
    print(ctab_pct.round(3))
    print(f"\nSaved risk tier distribution to: {ctab_path}")

    fig, ax = plt.subplots(figsize=(8, 4))

    x = np.arange(len(ctab_pct.index))
    bottom = np.zeros(len(ctab_pct.index))
    handles = {}

    for tier in ["Low", "Medium", "High"]:
        bars = ax.bar(x, ctab_pct[tier].values, bottom=bottom)
        bottom = bottom + ctab_pct[tier].values
        handles[tier] = bars[0]

    ax.set_ylabel("Proportion of apps")
    ax.set_xlabel("App category")
    ax.set_title(
        "Risk tier distribution by category (Top 20)\n"
        f"Low < {THRESH_LOW:.2f}, "
        f"{THRESH_LOW:.2f} ≤ Medium < {THRESH_HIGH:.2f}, "
        f"High ≥ {THRESH_HIGH:.2f}"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(ctab_pct.index, rotation=45, ha="right")
    ax.legend(handles.values(), handles.keys(), title="Risk tier", loc="upper right")

    plt.tight_layout()
    fig.savefig(FIG_RISK_TIER_CATEGORY, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved Figure to: {FIG_RISK_TIER_CATEGORY}")


def reproduce_appendix_popularity(df):
    df = df.copy()

    if "reviews" in df.columns:
        df["reviews_num"] = df["reviews"].apply(parse_km)
    else:
        df["reviews_num"] = np.nan

    if "downloads" in df.columns:
        df["downloads_num"] = df["downloads"].apply(parse_km)
    else:
        df["downloads_num"] = np.nan

    if "rating" in df.columns:
        pop_rating = df.dropna(subset=["rating", "SRS-O-weighted"])

        if not pop_rating.empty:
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.scatter(pop_rating["rating"], pop_rating["SRS-O-weighted"], alpha=0.5)

            ax.set_xlabel("App rating")
            ax.set_ylabel("SRS-O-weighted")
            ax.set_title("Popularity vs Risk: Rating vs Sensitivity Risk Score")

            plt.tight_layout()
            fig.savefig(FIG_RATING_RISK, dpi=300, bbox_inches="tight")
            plt.close(fig)

            print(f"Saved Appendix popularity figure to: {FIG_RATING_RISK}")
        else:
            print("No valid data for rating vs SRS-O-weighted plot.")
    else:
        print("Column 'rating' not found; skipping rating plot.")

    pop_down = df.dropna(subset=["downloads_num", "SRS-O-weighted"])
    pop_down = pop_down[pop_down["downloads_num"] > 0]

    if not pop_down.empty:
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(np.log10(pop_down["downloads_num"]), pop_down["SRS-O-weighted"], alpha=0.5)

        ax.set_xlabel("log10(Downloads)")
        ax.set_ylabel("SRS-O-weighted")
        ax.set_title("Popularity vs Risk: Downloads vs Sensitivity Risk Score")

        plt.tight_layout()
        fig.savefig(FIG_DOWNLOADS_RISK, dpi=300, bbox_inches="tight")
        plt.close(fig)

        print(f"Saved Appendix popularity figure to: {FIG_DOWNLOADS_RISK}")
    else:
        print("No valid data for downloads vs SRS-O-weighted plot.")

    corr_cols = ["SRS-O-weighted", "rating", "reviews_num", "downloads_num"]
    corr_cols = [col for col in corr_cols if col in df.columns]

    corr = df[corr_cols].corr().round(3)

    corr_path = os.path.join(RESULTS_DIR, "srs_popularity_correlation_matrix.csv")
    corr.to_csv(corr_path)

    print("\nCorrelation matrix (SRS vs popularity metrics):")
    print(corr)
    print(f"\nSaved correlation matrix to: {corr_path}")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    df = load_data()

    reproduce_rq4_category_risk(df)
    reproduce_appendix_popularity(df)


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(OUTPUT_LOG, "w", encoding="utf-8") as log_file:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log_file)

        try:
            main()
        finally:
            sys.stdout = original_stdout