"""
P0-1 三评分者 ICC 分析：3 位专家盲评 vs Claude judge vs GPT judge

输入文件：
  - blind_review/rating_sheet.md          (Rater 1: 第一作者 / CNAS 主任技师)
  - blind_review/rating_sheet_rater2.md   (Rater 2: 内审员)
  - blind_review/rating_sheet_rater3.md   (Rater 3: 内审员)
  - blind_review/key.json
  - cnas_judge_final_15tasks.json + h_claude_judge_supplement.json
  - gpt_judge_summary.json

输出：
  - 每篇 5-rater 矩阵（3 专家 + Claude + GPT），每维度 + 均值
  - 专家间一致性：Fleiss κ（连续版——ICC(2,k) + ICC(3,k)）
  - 3 专家均值 vs LLM judge 的 ICC / Pearson / Spearman
  - 按组的专家均值排名
  - blind_review/icc_results_3raters.json
"""

import json
import re
import statistics
from pathlib import Path

import pandas as pd
import pingouin as pg

BASE = Path(__file__).resolve().parent
BLIND = BASE / "blind_review"
KEY_FILE = BLIND / "key.json"
SHEETS = {
    "rater1": BLIND / "rating_sheet.md",
    "rater2": BLIND / "rating_sheet_rater2.md",
    "rater3": BLIND / "rating_sheet_rater3.md",
}
CLAUDE_JUDGE = BASE / "cnas_judge_final_15tasks.json"
CLAUDE_SUPPLEMENT = BASE / "h_claude_judge_supplement.json"
GPT_JUDGE = BASE / "gpt_judge_summary.json"

DIMS = ["条款满足度", "可操作性", "内部一致性", "PDCA闭环", "专业深度"]
DIM_ALIASES = {
    "条款满足度": "条款满足度",
    "可操作性": "可操作性",
    "内部一致性": "内部一致性",
    "PDCA闭环": "PDCA闭环",
    "PDCA 闭环": "PDCA闭环",
    "专业深度": "专业深度",
}
CLAUDE_GROUP_ALIAS = {
    "E_rules_v2": "E_rules",
    "G_template_rules": "G_combined",
}


def parse_rating_sheet(path: Path) -> dict[str, dict[str, float]]:
    """支持整数或小数评分。"""
    text = path.read_text(encoding="utf-8")
    results = {}
    current_paper = None
    current_scores = {}

    for line in text.splitlines():
        m_paper = re.match(r"^##\s+(paper_\d{2})", line.strip())
        if m_paper:
            if current_paper and current_scores:
                results[current_paper] = current_scores
            current_paper = m_paper.group(1)
            current_scores = {}
            continue

        m_row = re.match(r"^\|\s*\d+\.\s*([^|]+?)\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*\|", line)
        if m_row and current_paper:
            dim_raw = m_row.group(1).strip()
            score = float(m_row.group(2))
            dim_key = None
            for alias, canon in DIM_ALIASES.items():
                if alias in dim_raw or dim_raw in alias:
                    dim_key = canon
                    break
            if dim_key:
                current_scores[dim_key] = score

    if current_paper and current_scores:
        results[current_paper] = current_scores

    return results


def get_claude_scores(claude_data, supp, group, task, rep):
    for row in supp.get("scores", []):
        if row["group"] == group and row["task"] == task and row["rep"] == rep:
            return {d: row["dims"][d]["score"] for d in DIMS}
    lookup = CLAUDE_GROUP_ALIAS.get(group, group)
    try:
        arr = claude_data["data"][task][lookup][rep - 1]
        return dict(zip(DIMS, arr))
    except (KeyError, IndexError):
        return None


def get_gpt_scores(gpt_data, group, task, rep):
    for row in gpt_data:
        if row["group"] == group and row["task"] == task and row["rep"] == rep:
            return {d: row[d] for d in DIMS}
    return None


def compute_icc_pair(df, rater_a, rater_b, label):
    sub = df[[rater_a, rater_b]].dropna()
    if len(sub) < 3:
        print(f"\n### {label}  ⚠️ n={len(sub)} 样本不足")
        return None

    sub = sub.reset_index(drop=True).copy()
    sub["target"] = range(len(sub))
    long = sub.melt(id_vars="target", value_vars=[rater_a, rater_b],
                    var_name="rater", value_name="rating")
    icc = pg.intraclass_corr(data=long, targets="target", raters="rater", ratings="rating")
    icc_21 = icc[icc["Type"] == "ICC(A,1)"].iloc[0]
    icc_31 = icc[icc["Type"] == "ICC(C,1)"].iloc[0]
    ci21 = icc_21["CI95%"] if "CI95%" in icc_21.index else icc_21.get("CI95", [None, None])
    ci31 = icc_31["CI95%"] if "CI95%" in icc_31.index else icc_31.get("CI95", [None, None])

    r_pearson = sub[rater_a].corr(sub[rater_b], method="pearson")
    r_spearman = sub[rater_a].corr(sub[rater_b], method="spearman")
    diff_mean = (sub[rater_a] - sub[rater_b]).mean()

    print(f"\n### {label}  (n={len(sub)})")
    print(f"  ICC(2,1) = {icc_21['ICC']:.3f}   95% CI [{ci21[0]:.3f}, {ci21[1]:.3f}]  p={icc_21['pval']:.4f}")
    print(f"  ICC(3,1) = {icc_31['ICC']:.3f}   95% CI [{ci31[0]:.3f}, {ci31[1]:.3f}]  p={icc_31['pval']:.4f}")
    print(f"  Pearson  r = {r_pearson:.3f}   Spearman ρ = {r_spearman:.3f}")
    print(f"  Mean diff ({rater_a} − {rater_b}) = {diff_mean:+.3f}")

    return {"n": int(len(sub)),
            "ICC21": float(icc_21["ICC"]), "ICC31": float(icc_31["ICC"]),
            "pearson": float(r_pearson), "spearman": float(r_spearman),
            "diff": float(diff_mean)}


def compute_icc_multi(df, raters, label):
    """k 个评分者的 ICC(2,k) 和 ICC(3,k)：全体一致性。"""
    sub = df[raters].dropna()
    if len(sub) < 3:
        print(f"\n### {label}  ⚠️ n={len(sub)} 样本不足")
        return None
    sub = sub.reset_index(drop=True).copy()
    sub["target"] = range(len(sub))
    long = sub.melt(id_vars="target", value_vars=raters, var_name="rater", value_name="rating")
    icc = pg.intraclass_corr(data=long, targets="target", raters="rater", ratings="rating")

    print(f"\n### {label}  (n={len(sub)}, k={len(raters)} raters)")
    for icc_type in ["ICC(A,1)", "ICC(C,1)", "ICC(A,k)", "ICC(C,k)"]:
        row = icc[icc["Type"] == icc_type].iloc[0]
        ci = row["CI95%"] if "CI95%" in row.index else row.get("CI95", [None, None])
        name = {"ICC(A,1)": "ICC(2,1) single",
                "ICC(C,1)": "ICC(3,1) single",
                "ICC(A,k)": "ICC(2,k) avg  ",
                "ICC(C,k)": "ICC(3,k) avg  "}[icc_type]
        print(f"  {name} = {row['ICC']:.3f}   95% CI [{ci[0]:.3f}, {ci[1]:.3f}]  p={row['pval']:.4f}")

    return {
        "n": int(len(sub)), "k": len(raters),
        "ICC_2_1": float(icc[icc["Type"] == "ICC(A,1)"].iloc[0]["ICC"]),
        "ICC_3_1": float(icc[icc["Type"] == "ICC(C,1)"].iloc[0]["ICC"]),
        "ICC_2_k": float(icc[icc["Type"] == "ICC(A,k)"].iloc[0]["ICC"]),
        "ICC_3_k": float(icc[icc["Type"] == "ICC(C,k)"].iloc[0]["ICC"]),
    }


def interpret_icc(icc):
    if icc is None: return "n/a"
    if icc < 0.50: return "差"
    if icc < 0.75: return "中等"
    if icc < 0.90: return "好"
    return "优"


def main():
    # 1) 加载三位专家评分
    raters = {}
    for name, path in SHEETS.items():
        if not path.exists():
            print(f"❌ 未找到 {path}")
            return
        raters[name] = parse_rating_sheet(path)

    key = {r["blind_id"]: r for r in json.load(open(KEY_FILE))}
    claude_data = json.load(open(CLAUDE_JUDGE))
    claude_supp = json.load(open(CLAUDE_SUPPLEMENT)) if CLAUDE_SUPPLEMENT.exists() else {"scores": []}
    gpt_data = json.load(open(GPT_JUDGE))

    # 2) 组装每篇的完整评分矩阵
    rows = []
    for blind_id, meta in sorted(key.items()):
        row = {"blind_id": blind_id, "group": meta["group"], "task": meta["task"], "rep": meta["rep"]}
        complete = True
        for rater_name, rater_scores in raters.items():
            s = rater_scores.get(blind_id, {})
            if not all(d in s for d in DIMS):
                complete = False
                print(f"⚠️ {rater_name} on {blind_id}: missing dims")
                continue
            row[f"{rater_name}_mean"] = statistics.mean(s.values())
            for d in DIMS:
                row[f"{rater_name}_{d}"] = s[d]

        c = get_claude_scores(claude_data, claude_supp, meta["group"], meta["task"], meta["rep"])
        g = get_gpt_scores(gpt_data, meta["group"], meta["task"], meta["rep"])
        row["claude_mean"] = statistics.mean(c.values()) if c else None
        row["gpt_mean"] = statistics.mean(g.values()) if g else None

        rows.append(row)

    df = pd.DataFrame(rows)
    df["expert_mean"] = df[["rater1_mean", "rater2_mean", "rater3_mean"]].mean(axis=1)
    df["llm_mean"] = df[["claude_mean", "gpt_mean"]].mean(axis=1)

    print(f"\n=== 共 {len(df)} 篇完整评分 ===\n")

    # 3) 每篇一览
    print("### 每篇 5 评分者分数（专家 1/2/3 + Claude + GPT）\n")
    hdr = f"{'paper':<10} {'组':<22} {'任务':<4} {'R1':>5} {'R2':>5} {'R3':>5} {'专家均':>6} {'Claude':>7} {'GPT':>5}"
    print(hdr); print("-" * len(hdr))
    for _, r in df.iterrows():
        print(f"{r['blind_id']:<10} {r['group']:<22} {r['task']:<4} "
              f"{r['rater1_mean']:>5.2f} {r['rater2_mean']:>5.2f} {r['rater3_mean']:>5.2f} "
              f"{r['expert_mean']:>6.2f} {r['claude_mean']:>7.2f} {r['gpt_mean']:>5.2f}")

    # 4) 专家间一致性
    print("\n" + "=" * 70)
    print("## 专家间一致性（Inter-Rater Reliability）")
    print("=" * 70)
    results = {}
    results["expert_panel"] = compute_icc_multi(df, ["rater1_mean", "rater2_mean", "rater3_mean"],
                                                "3-Rater 专家组")
    results["r1_vs_r2"] = compute_icc_pair(df, "rater1_mean", "rater2_mean", "Rater1 vs Rater2")
    results["r1_vs_r3"] = compute_icc_pair(df, "rater1_mean", "rater3_mean", "Rater1 vs Rater3")
    results["r2_vs_r3"] = compute_icc_pair(df, "rater2_mean", "rater3_mean", "Rater2 vs Rater3")

    # 5) 专家均值 vs LLM judge
    print("\n" + "=" * 70)
    print("## 专家均值 vs LLM Judge")
    print("=" * 70)
    results["expert_vs_claude"] = compute_icc_pair(df, "expert_mean", "claude_mean", "专家均值 vs Claude")
    results["expert_vs_gpt"] = compute_icc_pair(df, "expert_mean", "gpt_mean", "专家均值 vs GPT")
    results["expert_vs_llm_mean"] = compute_icc_pair(df, "expert_mean", "llm_mean", "专家均值 vs LLM 均值")
    results["claude_vs_gpt"] = compute_icc_pair(df, "claude_mean", "gpt_mean", "Claude vs GPT（参照）")

    # 6) 按组排名
    print("\n" + "=" * 70)
    print("## 按配置组的专家均值排名（组 n=1 或 2）")
    print("=" * 70)
    by_group = df.groupby("group").agg(
        n=("blind_id", "count"),
        expert_mean=("expert_mean", "mean"),
        rater1_mean=("rater1_mean", "mean"),
        rater2_mean=("rater2_mean", "mean"),
        rater3_mean=("rater3_mean", "mean"),
        claude_mean=("claude_mean", "mean"),
        gpt_mean=("gpt_mean", "mean"),
    ).sort_values("expert_mean", ascending=False)
    print(by_group.round(3))

    # 7) 保存
    out = BLIND / "icc_results_3raters.json"
    out_dict = {
        "n_papers": int(len(df)),
        "per_paper": df.round(3).to_dict("records"),
        "by_group": by_group.round(3).reset_index().to_dict("records"),
        "icc": results,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(out_dict, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n✅ 结果保存至 {out}")

    # 8) 一句话结论
    print("\n" + "=" * 70)
    print("## 结论速递")
    print("=" * 70)
    panel = results.get("expert_panel", {})
    ec = results.get("expert_vs_claude", {})
    eg = results.get("expert_vs_gpt", {})
    print(f"  3 位专家间一致性 ICC(2,k)={panel.get('ICC_2_k'):.3f} ({interpret_icc(panel.get('ICC_2_k'))})")
    print(f"  专家均值 vs Claude ICC(3,1)={ec.get('ICC31'):.3f} (mean diff={ec.get('diff'):+.2f})")
    print(f"  专家均值 vs GPT    ICC(3,1)={eg.get('ICC31'):.3f} (mean diff={eg.get('diff'):+.2f})")


if __name__ == "__main__":
    main()
