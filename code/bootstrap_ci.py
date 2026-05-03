"""
Bootstrap 95% CI reproduction script for §3.2 four-component ablation.

Method: nonparametric percentile bootstrap (B=10,000 resamples; seed=42),
        independently resampling each group with replacement using
        numpy.random.choice; CI limits are the 2.5th/97.5th percentiles of
        the resampled Δ = mean(group_B) − mean(group_A) distribution.

Inputs (relative to the script's own directory):
    gpt_judge_summary.json — per-document GPT-judge mean ratings
                             (one rating per document, 0–5 Likert scale).
                             Each row is a dict with at least: group, mean.
                             Rows whose group starts with "gpt4o_" denote
                             GPT-generated documents and are excluded; the
                             ablation in §3.2 is defined on the 405
                             Claude-generated documents only.

Output: prints Δ and 95% CI for the four pre-specified contrasts, matching
        the values reported in §3.2 of the manuscript.

Usage:
    python3 bootstrap_ci.py
"""

import json
from pathlib import Path

import numpy as np


CONTRASTS = [
    ("rules",          "A_bare",           "E_rules_v2"),
    ("skeleton",       "E_rules_v2",       "H4_sop_only"),
    ("detailed",       "H3_skeleton",      "G_template_rules"),
    ("examples",       "G_template_rules", "H2_keep_examples"),
]


def load_per_document_scores(json_path: Path) -> dict[str, np.ndarray]:
    """Load Claude-generated per-document GPT-judge means, grouped by configuration."""
    rows = json.loads(json_path.read_text())
    groups: dict[str, list[float]] = {}
    for r in rows:
        if r["group"].startswith("gpt4o_"):
            continue  # GPT-generated; out of scope for §3.2
        groups.setdefault(r["group"], []).append(r["mean"])
    return {g: np.asarray(v, dtype=float) for g, v in groups.items()}


def bootstrap_ci(a: np.ndarray, b: np.ndarray, B: int = 10_000, seed: int = 42) -> tuple[float, float, float]:
    """Return (Δ, ci_low, ci_high) using nonparametric percentile bootstrap."""
    rng = np.random.default_rng(seed)
    deltas = np.empty(B, dtype=float)
    for i in range(B):
        sa = rng.choice(a, size=len(a), replace=True)
        sb = rng.choice(b, size=len(b), replace=True)
        deltas[i] = sb.mean() - sa.mean()
    return b.mean() - a.mean(), float(np.percentile(deltas, 2.5)), float(np.percentile(deltas, 97.5))


def main() -> None:
    here = Path(__file__).resolve().parent
    candidates = [
        here / "gpt_judge_summary.json",
        here.parent / "data" / "scores" / "gpt_judge_summary.json",
    ]
    json_path = next((p for p in candidates if p.exists()), None)
    if json_path is None:
        raise FileNotFoundError(
            "gpt_judge_summary.json not found. Searched: "
            + ", ".join(str(p) for p in candidates)
        )
    groups = load_per_document_scores(json_path)

    print(f"{'contrast':<10} {'pair':<40} {'Δ':>8} {'95% CI':>20}")
    print("-" * 80)
    for name, a_grp, b_grp in CONTRASTS:
        delta, lo, hi = bootstrap_ci(groups[a_grp], groups[b_grp])
        print(f"{name:<10} {f'{b_grp} vs {a_grp}':<40} {delta:+8.3f} {f'[{lo:+.3f}, {hi:+.3f}]':>20}")


if __name__ == "__main__":
    main()
