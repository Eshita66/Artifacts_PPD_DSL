
import os
import pandas as pd

# CONFIG
XLSX_PATH = "../data/srs/ppd_ds_comparison_with_verdicts_appscore_1460.xlsx"
SHEET_NAME = "Verdicts"

RESULTS_DIR = "../results"

OUTPUT_XLSX = os.path.join(RESULTS_DIR, "alpha_sensitivity_results.xlsx")
OUTPUT_CSV = os.path.join(RESULTS_DIR, "alpha_sensitivity_summary.csv")

CATEGORY_WEIGHTS = {
    "Location": 3,
    "Personal info": 3,
    "Financial info": 3,
    "Health and fitness": 3,
    "Messages": 3,
    "Photos and videos": 3,
    "Audio": 3,
    "Files and docs": 2,
    "Calendar": 1,
    "Contacts": 3,
    "App activity": 2,
    "Web browsing": 3,
    "App info and performance": 1,
    "Device or other IDs": 3,
}

ALPHAS = [0.4, 0.5, 0.6, 0.7]

THRESH_LOW = 0.30
THRESH_HIGH = 0.70


def assign_tier(score):
    if pd.isna(score):
        return "NA"
    if score < THRESH_LOW:
        return "Low"
    elif score < THRESH_HIGH:
        return "Medium"
    else:
        return "High"


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET_NAME)

    required_cols = ["appname", "Operation", "Category", "verdict"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["is_mis"] = df["verdict"].isin(["UNDER", "OVER"]).astype(int)
    df["weight"] = df["Category"].map(CATEGORY_WEIGHTS).fillna(1)
    df["risk_contrib"] = df["weight"] * df["is_mis"]

    agg = (
        df.groupby(["appname", "Operation"], as_index=False)
        .agg(
            weighted_mismatch=("risk_contrib", "sum"),
            total_weight=("weight", "sum"),
        )
    )

    agg["SRS"] = agg["weighted_mismatch"] / agg["total_weight"]

    srs_wide = agg.pivot(index="appname", columns="Operation", values="SRS")

    srs_wide = srs_wide.rename(
        columns={
            "collected": "SRS-C",
            "shared": "SRS-S",
        }
    ).reset_index()

    srs_wide["SRS-O"] = srs_wide[["SRS-C", "SRS-S"]].mean(axis=1, skipna=True)

    for alpha in ALPHAS:
        score_col = f"SRS-O-w-alpha-{alpha}"
        tier_col = f"Tier-alpha-{alpha}"

        srs_wide[score_col] = (
            alpha * srs_wide["SRS-S"].fillna(0.0)
            + (1.0 - alpha) * srs_wide["SRS-C"].fillna(0.0)
        )

        srs_wide[tier_col] = srs_wide[score_col].apply(assign_tier)

    baseline_tier = srs_wide["Tier-alpha-0.6"]

    summary_rows = []

    for alpha in ALPHAS:
        tier_col = f"Tier-alpha-{alpha}"
        tiers = srs_wide[tier_col]
        total = len(tiers)

        low = (tiers == "Low").sum()
        medium = (tiers == "Medium").sum()
        high = (tiers == "High").sum()
        same = (tiers == baseline_tier).sum()

        summary_rows.append({
            "Alpha (sharing weight)": alpha,
            "Low apps": low,
            "Low (%)": round(low / total * 100, 2),
            "Medium apps": medium,
            "Medium (%)": round(medium / total * 100, 2),
            "High apps": high,
            "High (%)": round(high / total * 100, 2),
            "Same tier as baseline apps": same,
            "Same tier as baseline (%)": round(same / total * 100, 2),
        })

    alpha_summary = pd.DataFrame(summary_rows)

    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="w") as writer:
        srs_wide.to_excel(writer, sheet_name="Alpha_all_app_scores", index=False)
        alpha_summary.to_excel(writer, sheet_name="Alpha_sensitivity_summary", index=False)

    alpha_summary.to_csv(OUTPUT_CSV, index=False)

   
    print(f"Input file: {XLSX_PATH}")
    print(f"Saved Excel output: {OUTPUT_XLSX}")
    print(f"Saved summary CSV: {OUTPUT_CSV}")
    print("\nAlpha sensitivity summary:")
    print(alpha_summary)


if __name__ == "__main__":
    main()

