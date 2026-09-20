"""Reproduce Table 1 scores from released per-document scores, without API calls.

Population: Claude-generated outputs only, 15 tasks x 3 repeats per configuration.
For each configuration, average auto_weighted and GPT-judge mean separately.
Min-max normalize each set of nine configuration means, then average the two
normalized components with equal weight. Claude-judge scores are not a component.

Inputs: data/scores/all_scores_{6groups,h2h3,h4}.json and gpt_judge_summary.json.
Outputs: reproduced/table1_ranking.{json,csv}, or a separate --output-dir.
Context-token counts are deliberately not inferred from the scoring records.
"""

import argparse
import csv
import json
from pathlib import Path
import statistics


BASE = Path(__file__).resolve().parents[1]
SCORES = BASE / "data" / "scores"
GROUPS = (
    "A_bare", "B_simple", "C_full", "E_rules_v2", "F_template",
    "G_template_rules", "H2_keep_examples", "H3_skeleton", "H4_sop_only",
)
AUTO_FILES = ("all_scores_6groups.json", "all_scores_h2h3.json", "all_scores_h4.json")


def reproduce_ranking():
    auto = {group: {} for group in GROUPS}
    gpt = {group: {} for group in GROUPS}
    for filename in AUTO_FILES:
        for row in json.loads((SCORES / filename).read_text(encoding="utf-8")):
            group = row["group"]
            rep = int(Path(row["file"]).stem.rsplit("-", 1)[1])
            key = (row["task"], rep)
            if key in auto[group]:
                raise ValueError(f"Duplicate automatic score: {group}, {key}")
            auto[group][key] = row["auto_weighted"]

    for row in json.loads((SCORES / "gpt_judge_summary.json").read_text(encoding="utf-8")):
        group = row["group"]
        if group not in GROUPS:
            continue  # Separate GPT-generated robustness outputs are out of scope.
        key = (row["task"], row["rep"])
        if key in gpt[group]:
            raise ValueError(f"Duplicate GPT judge score: {group}, {key}")
        gpt[group][key] = row["mean"]

    expected = {(f"{category}{task}", rep) for category in "ABC"
                for task in range(1, 6) for rep in range(1, 4)}
    ranking = []
    for group in GROUPS:
        if set(auto[group]) != expected or set(gpt[group]) != expected:
            raise ValueError(f"{group}: expected the same 15 tasks x 3 repeats for both components")
        ranking.append({
            "group": group,
            "n_auto": len(auto[group]),
            "n_gpt_judge": len(gpt[group]),
            "auto_mean": statistics.mean(auto[group].values()),
            "gpt_judge_mean": statistics.mean(gpt[group].values()),
        })

    for component in ("auto", "gpt_judge"):
        values = [row[f"{component}_mean"] for row in ranking]
        low, high = min(values), max(values)
        if high == low:
            raise ValueError(f"Cannot min-max normalize constant {component} group means")
        for row in ranking:
            row[f"{component}_normalized"] = (row[f"{component}_mean"] - low) / (high - low)
    for row in ranking:
        row["composite"] = 0.5 * (row["auto_normalized"] + row["gpt_judge_normalized"])
    ranking.sort(key=lambda row: (-row["composite"], row["group"]))
    for rank, row in enumerate(ranking, start=1):
        row["rank"] = rank

    return {
        "population": "Claude-generated outputs; 15 tasks x 3 repeats x 9 configurations",
        "n_outputs": sum(row["n_auto"] for row in ranking),
        "method": "0.5 * minmax(group mean auto_weighted) + 0.5 * minmax(group mean GPT judge)",
        "normalization_scope": "Nine configuration means, separately for each component",
        "input_files": [f"data/scores/{name}" for name in (*AUTO_FILES, "gpt_judge_summary.json")],
        "ranking": ranking,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=BASE / "reproduced")
    args = parser.parse_args(argv)
    output_dir = args.output_dir.resolve()
    if output_dir.is_relative_to(BASE / "data"):
        parser.error("Output directory must be outside released data/")

    result = reproduce_ranking()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "table1_ranking.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    csv_path = output_dir / "table1_ranking.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result["ranking"][0]))
        writer.writeheader()
        writer.writerows(result["ranking"])
    for row in result["ranking"]:
        print(f"{row['rank']:>2}. {row['group']:<22} {row['composite']:.9f}")
    print(f"Saved {json_path} and {csv_path}")


if __name__ == "__main__":
    main()
