import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



EXCEL_PATH = "../data/prevalence/ppd_ds_comparison_with_verdicts_1460.xlsx"
SHEET_NAME = "Verdicts"

RESULTS_DIR = "../results"
FIGURES_DIR = "../figures"

OUTPUT_LOG = os.path.join(RESULTS_DIR, "prevalence_console_output.txt")

FIG_OVERALL_CONSISTENCY = os.path.join(FIGURES_DIR, "overall_consistency.png")
FIG_MISALIGNMENT_HEATMAP = os.path.join(FIGURES_DIR, "misalignment_heatmap.png")
FIG_CATEGORY_DSL_ONLY = os.path.join(FIGURES_DIR, "category_level_under.png")
FIG_CATEGORY_PPD_ONLY = os.path.join(FIGURES_DIR, "category_level_over.png")



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


def load_data() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

    required_cols = ["appname", "Operation", "Category", "verdict"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["is_under"] = (df["verdict"] == "UNDER").astype(int)
    df["is_over"] = (df["verdict"] == "OVER").astype(int)
    df["is_mis"] = df["verdict"].isin(["UNDER", "OVER"]).astype(int)

    return df



def compute_cell_level_stats(df: pd.DataFrame):
    overall = (
        df.groupby("Operation")[["is_mis", "is_under", "is_over"]]
        .sum()
    )

    counts = df.groupby("Operation").size().rename("N_cells")
    overall = overall.join(counts)

    overall["misalign_rate"] = overall["is_mis"] / overall["N_cells"]
    overall["under_rate"] = overall["is_under"] / overall["N_cells"]
    overall["over_rate"] = overall["is_over"] / overall["N_cells"]
    overall["agree_rate"] = 1.0 - overall["misalign_rate"]

    cat_stats = (
        df.groupby(["Operation", "Category"])[["is_mis", "is_under", "is_over"]]
        .sum()
    )

    cat_counts = df.groupby(["Operation", "Category"]).size().rename("N_cells")
    cat_stats = cat_stats.join(cat_counts)

    cat_stats["misalign_rate"] = cat_stats["is_mis"] / cat_stats["N_cells"]
    cat_stats["under_rate"] = cat_stats["is_under"] / cat_stats["N_cells"]
    cat_stats["over_rate"] = cat_stats["is_over"] / cat_stats["N_cells"]

    return overall, cat_stats


def compute_app_level_stats(df: pd.DataFrame):
    app_op = (
        df.groupby(["appname", "Operation"])[["is_mis", "is_under", "is_over"]]
        .max()
        .reset_index()
    )

    app_overall = (
        app_op.groupby("Operation")[["is_mis", "is_under", "is_over"]]
        .sum()
    )

    n_apps = app_op.groupby("Operation")["appname"].nunique().rename("N_apps")
    app_overall = app_overall.join(n_apps)

    app_overall = app_overall.rename(columns={
        "is_mis": "any_mis_app",
        "is_under": "any_under_app",
        "is_over": "any_over_app",
    })

    app_overall["misalign_rate_app"] = app_overall["any_mis_app"] / app_overall["N_apps"]
    app_overall["under_rate_app"] = app_overall["any_under_app"] / app_overall["N_apps"]
    app_overall["over_rate_app"] = app_overall["any_over_app"] / app_overall["N_apps"]

    return app_overall




def plot_overall_consistency(overall: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))

    ops = overall.index.tolist()
    x = np.arange(len(ops))

    agreement = overall["agree_rate"].values
    dsl_only = overall["under_rate"].values
    ppd_only = overall["over_rate"].values

    width = 0.25
    x_agree = x - width
    x_dsl = x
    x_ppd = x + width

    ax.bar(x_agree, agreement, width=width, label="Agreement (PPD = DSL)")
    ax.bar(x_dsl, dsl_only, width=width, label="Misalignment in DSL only")
    ax.bar(x_ppd, ppd_only, width=width, label="Misalignment in PPD only")

    ax.set_ylim(0, 1)

    def add_pct_labels(x_positions, heights):
        eps = 0.01
        for xi, h in zip(x_positions, heights):
            label = f"{h * 100:.1f}%"
            y = h + eps
            va = "bottom"

            if y >= 1.0 - eps:
                y = h - eps
                va = "top"

            ax.text(xi, y, label, ha="center", va=va, fontsize=9)

    add_pct_labels(x_agree, agreement)
    add_pct_labels(x_dsl, dsl_only)
    add_pct_labels(x_ppd, ppd_only)

    ax.set_xticks(x)
    ax.set_xticklabels(ops)
    ax.set_xlabel("Data Operation")
    ax.set_ylabel("Rate (over app-data-category)")
    ax.set_title("Agreement vs Misalignment by Data Operation")
    ax.legend()

    plt.tight_layout()
    fig.savefig(FIG_OVERALL_CONSISTENCY, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved Figure 2 to: {FIG_OVERALL_CONSISTENCY}")



def plot_misalignment_heatmap(cat_stats: pd.DataFrame):
    cat_stats_reset = cat_stats.reset_index()

    cat_mis_heat = cat_stats_reset.pivot(
        index="Category",
        columns="Operation",
        values="misalign_rate"
    )

    columns_in_order = [c for c in ["collected", "shared"] if c in cat_mis_heat.columns]
    cat_mis_heat = cat_mis_heat[columns_in_order]

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(cat_mis_heat.values, aspect="auto")

    ax.set_xticks(range(len(cat_mis_heat.columns)))
    ax.set_xticklabels(cat_mis_heat.columns)

    ax.set_yticks(range(len(cat_mis_heat.index)))
    ax.set_yticklabels(cat_mis_heat.index)

    ax.set_title("Misalignment in ALL by Data Category and Operation")

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Misalignment in ALL rate")

    plt.tight_layout()
    fig.savefig(FIG_MISALIGNMENT_HEATMAP, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved Figure 4 to: {FIG_MISALIGNMENT_HEATMAP}")



def plot_category_bars(cat_stats: pd.DataFrame):
    cat_stats_reset = cat_stats.reset_index()

    metrics = [
        (
            "under_rate",
            "Category-level Misalignment in DSL only (PPD vs DSL)",
            "Misalignment in DSL only Rate",
            FIG_CATEGORY_DSL_ONLY
        ),
        (
            "over_rate",
            "Category-level Misalignment in PPD only (PPD vs DSL)",
            "Misalignment in PPD only Rate",
            FIG_CATEGORY_PPD_ONLY
        ),
    ]

    for metric_col, title, ylabel, outfile in metrics:
        cat_metric = cat_stats_reset.pivot(
            index="Category",
            columns="Operation",
            values=metric_col
        )

        columns_in_order = [c for c in ["collected", "shared"] if c in cat_metric.columns]
        cat_metric = cat_metric[columns_in_order]

        categories = cat_metric.index.tolist()
        x = np.arange(len(categories))
        width = 0.35

        fig, ax = plt.subplots(figsize=(8, 5))

        if "collected" in cat_metric.columns:
            ax.bar(x - width / 2, cat_metric["collected"], width, label="Collected")

        if "shared" in cat_metric.columns:
            ax.bar(x + width / 2, cat_metric["shared"], width, label="Shared")

        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")
        ax.set_xlabel("Data category")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_ylim(0, 1)
        ax.legend()

        plt.tight_layout()
        fig.savefig(outfile, dpi=300, bbox_inches="tight")
        plt.close(fig)

        print(f"Saved category figure to: {outfile}")




def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    df = load_data()

    overall, cat_stats = compute_cell_level_stats(df)
    app_overall = compute_app_level_stats(df)

    print("Cell-level prevalence by operation:")
    print(overall)

    print("\nCategory-level prevalence:")
    print(cat_stats)

    print("\nApp-level prevalence by operation:")
    print(app_overall)

    overall.to_csv(os.path.join(RESULTS_DIR, "cell_level_prevalence_by_operation.csv"))
    cat_stats.to_csv(os.path.join(RESULTS_DIR, "category_level_prevalence.csv"))
    app_overall.to_csv(os.path.join(RESULTS_DIR, "app_level_prevalence_by_operation.csv"))

    print("\nSaved result tables to results folder.")

    plot_overall_consistency(overall)
    plot_misalignment_heatmap(cat_stats)
    plot_category_bars(cat_stats)


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(OUTPUT_LOG, "w", encoding="utf-8") as log_file:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log_file)

        try:
            main()
        finally:
            sys.stdout = original_stdout