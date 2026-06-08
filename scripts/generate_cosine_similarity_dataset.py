import json
from pathlib import Path
from typing import Dict, Set, List, Tuple
import pandas as pd
import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from category_mapping2 import parse_label_sections, parse_policy_items_with_trace


def cosine_sim(text1: str, text2: str) -> float:
    """Compute cosine similarity between two strings"""
    t1 = (text1 or "").strip()
    t2 = (text2 or "").strip()
    if not t1 or not t2:
        return 0.0

    vec = TfidfVectorizer().fit([t1, t2])
    X = vec.transform([t1, t2])
    return float(cosine_similarity(X[0:1], X[1:2])[0][0])


def aggregate_subtypes_by_section(parsed: Dict[str, Dict[str, Set[str]]]) -> Dict[str, Set[str]]:
    out = {"shared": set(), "collected": set()}

    for section in ["shared", "collected"]:
        cat_map = parsed.get(section, {})
        agg: Set[str] = set()

        for _cat, subs in cat_map.items():
            agg.update(subs)

        out[section] = agg

    out["both_sections"] = out["shared"] | out["collected"]
    return out


def build_global_rows_for_app(app: str, label_json: dict, policy_json: dict) -> List[dict]:
    label_parsed = parse_label_sections(label_json)
    policy_mapped, _, _ = parse_policy_items_with_trace(policy_json)

    label_global = aggregate_subtypes_by_section(label_parsed)
    policy_global = aggregate_subtypes_by_section(policy_mapped)

    rows = []

    for section in ["shared", "collected", "both_sections"]:
        L = set(label_global.get(section, set()))
        P = set(policy_global.get(section, set()))

        both = L & P
        only_policy = P - L
        only_label = L - P

        label_terms = sorted(L)
        policy_terms = sorted(P)

        label_text = " ".join(label_terms)
        policy_text = " ".join(policy_terms)

        cos = cosine_sim(label_text, policy_text)
        jaccard = (len(both) / len(L | P)) if (L or P) else 0.0

        rows.append({
            "app": app,
            "section_scope": section,
            "cosine_similarity": round(cos, 4),
            "jaccard_similarity": round(jaccard, 4),

            "both_declared_count": len(both),
            "only_policy_declared_count": len(only_policy),
            "only_label_declared_count": len(only_label),
            "label_total_subtypes": len(L),
            "policy_total_subtypes": len(P),

            "both_declared": ", ".join(sorted(both)) or "-",
            "only_policy_declared": ", ".join(sorted(only_policy)) or "-",
            "only_label_declared": ", ".join(sorted(only_label)) or "-",

            "label_terms_all": ", ".join(label_terms) or "-",
            "policy_terms_all": ", ".join(policy_terms) or "-",
        })

    return rows


def normalize_app_name(name: str) -> str:
    """Normalize app names across datasets for matching."""
    n = name.lower()
    n = re.sub(r"[^a-z0-9]+", "_", n)
    n = re.sub(r"_+", "_", n)
    return n.strip("_")


def build_matched_pairs(labels_all: dict, policies_all: dict) -> List[Tuple[str, str, str]]:
    labels_norm: Dict[str, List[str]] = defaultdict(list)
    for k in labels_all.keys():
        labels_norm[normalize_app_name(k)].append(k)

    policies_norm: Dict[str, List[str]] = defaultdict(list)
    for k in policies_all.keys():
        policies_norm[normalize_app_name(k)].append(k)

    common_norm = sorted(set(labels_norm.keys()) & set(policies_norm.keys()))
    if not common_norm:
        raise SystemExit("No overlapping apps in labels and policies JSONs (after normalization)")

    pairs: List[Tuple[str, str, str]] = []

    for nk in common_norm:
        label_originals = sorted(labels_norm[nk])
        policy_originals = sorted(policies_norm[nk])

        max_len = max(len(label_originals), len(policy_originals))

        for i in range(max_len):
            lk = label_originals[min(i, len(label_originals) - 1)]
            pk = policy_originals[min(i, len(policy_originals) - 1)]

            out_name = nk if max_len == 1 else f"{nk}__{i}" if i > 0 else nk
            pairs.append((out_name, lk, pk))

    return pairs


def run(labels_path: Path, policies_path: Path, out_csv: Path):
    labels_all = json.loads(Path(labels_path).read_text(encoding="utf-8"))
    policies_all = json.loads(Path(policies_path).read_text(encoding="utf-8"))

    matched_pairs = build_matched_pairs(labels_all, policies_all)
    print(f"Total matched app pairs: {len(matched_pairs)}")

    all_rows: List[dict] = []

    for app_name, label_key, policy_key in matched_pairs:
        rows = build_global_rows_for_app(
            app_name,
            labels_all[label_key],
            policies_all[policy_key],
        )
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)

    print(f"Saved GLOBAL label vs policy similarities → {out_csv}")
    print(f"Total apps: {df['app'].nunique()}")


if __name__ == "__main__":
    labels_file = Path(
        "../data/cosinesimilarity/dataSafetyData.json"
    )

    policies_file = Path(
        "../data/cosinesimilarity/privacifyData.json"
    )

    output_file = Path(
        "../data/cosinesimilarity/global_label_vs_policy_similarity1460.csv"
    )

    run(labels_file, policies_file, output_file)