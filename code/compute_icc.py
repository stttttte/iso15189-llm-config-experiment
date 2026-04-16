"""
P0-1 ICC 计算：用户盲评 vs Claude judge vs GPT judge

用法：
  # 用户评分完成后（rating_sheet.md 已填数字）：
  python3 compute_icc.py

输出：
  - 10 篇的 3 评分者矩阵（用户/Claude/GPT），每维度 + 总均值
  - ICC(2,1) 和 ICC(3,1)：用户 vs Claude / vs GPT / vs LLM 均值
  - 相关系数（Pearson, Spearman）
  - 配对差异分析（谁高谁低）
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
SHEET_FILE = BLIND / "rating_sheet.md"
CLAUDE_JUDGE = BASE / "cnas_judge_final_15tasks.json"
CLAUDE_SUPPLEMENT = BASE / "h_claude_judge_supplement.json"  # H 组补跑
GPT_JUDGE = BASE / "gpt_judge_summary.json"

DIMS = ["条款满足度", "可操作性", "内部一致性", "PDCA闭环", "专业深度"]
DIM_ALIASES = {  # 容错：表格里可能有不同写法
    "条款满足度": "条款满足度",
    "可操作性": "可操作性",
    "内部一致性": "内部一致性",
    "PDCA闭环": "PDCA闭环",
    "PDCA 闭环": "PDCA闭环",
    "专业深度": "专业深度",
}


def parse_rating_sheet(path: Path) -> dict[str, dict[str, int]]:
    """从 rating_sheet.md 提取评分。

    结构：
      ## paper_NN — 任务名
      | 维度 | 分数 | 理由 |
      |...   | N   | ... |
    """
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

        # 表格行：| X. 维度名 | 分数 | 理由 |  （分数可为整数或小数）
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


CLAUDE_GROUP_ALIAS = {
    "E_rules_v2": "E_rules",
    "G_template_rules": "G_combined",
}


def get_claude_scores(claude_data: dict, supplement: dict, group: str, task: str, rep: int) -> dict:
    """Claude judge: data[task][group][rep-1] = [5 dims in order]
    注意：Claude judge 使用旧组名（E_rules / G_combined），需映射。
    H 组（H2/H3/H4）从 supplement 读取（2026-04-14 补跑）。
    """
    # 先查 supplement
    for row in supplement.get("scores", []):
        if row["group"] == group and row["task"] == task and row["rep"] == rep:
            return {d: row["dims"][d]["score"] for d in DIMS}

    lookup = CLAUDE_GROUP_ALIAS.get(group, group)
    try:
        arr = claude_data["data"][task][lookup][rep - 1]
        return dict(zip(DIMS, arr))
    except (KeyError, IndexError):
        return None


def get_gpt_scores(gpt_data: list, group: str, task: str, rep: int) -> dict:
    """GPT judge: list of dicts"""
    for row in gpt_data:
        if row["group"] == group and row["task"] == task and row["rep"] == rep:
            return {d: row[d] for d in DIMS}
    return None


def compute_icc_pair(df: pd.DataFrame, rater_a: str, rater_b: str, label: str):
    """计算两评分者的 ICC。df: targets × raters 宽格式；转长格式后调用 pingouin"""
    sub = df[[rater_a, rater_b]].dropna()
    if len(sub) < 3:
        print(f"\n### {label}  ⚠️ n={len(sub)} 样本不足，跳过 ICC")
        return {"ICC21": None, "ICC31": None, "pearson": None, "spearman": None, "diff": None, "n": len(sub)}
    sub = sub.reset_index(drop=False).rename(columns={sub.index.name or "index": "target"})
    if "target" not in sub.columns:
        sub["target"] = range(len(sub))
    long = sub.melt(id_vars="target", value_vars=[rater_a, rater_b], var_name="rater", value_name="rating")
    icc = pg.intraclass_corr(data=long, targets="target", raters="rater", ratings="rating")
    # pingouin labels: ICC(A,1)=ICC(2,1), ICC(C,1)=ICC(3,1)
    icc_21 = icc[icc["Type"] == "ICC(A,1)"].iloc[0]
    icc_31 = icc[icc["Type"] == "ICC(C,1)"].iloc[0]

    r_pearson = sub[rater_a].corr(sub[rater_b], method="pearson")
    r_spearman = sub[rater_a].corr(sub[rater_b], method="spearman")
    diff_mean = (sub[rater_a] - sub[rater_b]).mean()

    print(f"\n### {label}  (n={len(sub)})")
    ci21 = icc_21["CI95%"] if "CI95%" in icc_21.index else icc_21.get("CI95", [None, None])
    ci31 = icc_31["CI95%"] if "CI95%" in icc_31.index else icc_31.get("CI95", [None, None])
    print(f"  ICC(2,1) = {icc_21['ICC']:.3f}   95% CI [{ci21[0]:.3f}, {ci21[1]:.3f}]  p={icc_21['pval']:.4f}")
    print(f"  ICC(3,1) = {icc_31['ICC']:.3f}   95% CI [{ci31[0]:.3f}, {ci31[1]:.3f}]  p={icc_31['pval']:.4f}")
    print(f"  Pearson  r = {r_pearson:.3f}")
    print(f"  Spearman ρ = {r_spearman:.3f}")
    print(f"  Mean diff ({rater_a} − {rater_b}) = {diff_mean:+.3f}")

    return {"n": len(sub), "ICC21": float(icc_21["ICC"]), "ICC31": float(icc_31["ICC"]),
            "pearson": float(r_pearson), "spearman": float(r_spearman), "diff": float(diff_mean)}


def interpret_icc(icc):
    if icc < 0.50: return "差 (poor)"
    if icc < 0.75: return "中等 (moderate)"
    if icc < 0.90: return "好 (good)"
    return "优 (excellent)"


def main():
    if not SHEET_FILE.exists():
        print(f"❌ 未找到评分表 {SHEET_FILE}")
        return
    if not KEY_FILE.exists():
        print(f"❌ 未找到 key.json {KEY_FILE}")
        return

    human = parse_rating_sheet(SHEET_FILE)
    key = {r["blind_id"]: r for r in json.load(open(KEY_FILE))}
    claude_data = json.load(open(CLAUDE_JUDGE))
    claude_supp = json.load(open(CLAUDE_SUPPLEMENT)) if CLAUDE_SUPPLEMENT.exists() else {"scores": []}
    gpt_data = json.load(open(GPT_JUDGE))

    rows = []
    incomplete = []
    for blind_id, meta in sorted(key.items()):
        h = human.get(blind_id, {})
        missing = [d for d in DIMS if d not in h]
        if missing:
            incomplete.append((blind_id, missing))
            continue

        c = get_claude_scores(claude_data, claude_supp, meta["group"], meta["task"], meta["rep"])
        g = get_gpt_scores(gpt_data, meta["group"], meta["task"], meta["rep"])

        row = {
            "blind_id": blind_id,
            "group": meta["group"],
            "task": meta["task"],
            "rep": meta["rep"],
            "human_mean": statistics.mean(h.values()),
            "claude_mean": statistics.mean(c.values()) if c else None,
            "gpt_mean": statistics.mean(g.values()) if g else None,
        }
        for d in DIMS:
            row[f"human_{d}"] = h[d]
            row[f"claude_{d}"] = c[d] if c else None
            row[f"gpt_{d}"] = g[d] if g else None
        rows.append(row)

    if incomplete:
        print("⚠️ 以下论文评分不完整，跳过：")
        for bid, miss in incomplete:
            print(f"   {bid}: 缺维度 {miss}")

    if not rows:
        print("❌ 没有可用评分，请先填写 rating_sheet.md")
        return

    df = pd.DataFrame(rows)
    print(f"\n=== 共 {len(df)} 篇完整评分 ===\n")

    # 每篇对比
    print("### 每篇三评分者均分（盲评编号 → 组名已解密）\n")
    print(f"{'paper':<10} {'组':<20} {'任务':<4} {'人':>5} {'Claude':>7} {'GPT':>5} {'人-C':>6} {'人-G':>6}")
    print("-" * 75)
    for _, r in df.iterrows():
        hc = r["human_mean"] - r["claude_mean"]
        hg = r["human_mean"] - r["gpt_mean"]
        print(f"{r['blind_id']:<10} {r['group']:<20} {r['task']:<4} "
              f"{r['human_mean']:>5.2f} {r['claude_mean']:>7.2f} {r['gpt_mean']:>5.2f} "
              f"{hc:>+6.2f} {hg:>+6.2f}")

    # ICC 基于每篇总均分
    means = df.set_index("blind_id")[["human_mean", "claude_mean", "gpt_mean"]].copy()
    means["llm_mean"] = (means["claude_mean"] + means["gpt_mean"]) / 2

    print("\n=== ICC (基于每篇 5 维度均分) ===")
    results = {}
    results["human_vs_claude"] = compute_icc_pair(means, "human_mean", "claude_mean", "人 vs Claude judge")
    results["human_vs_gpt"] = compute_icc_pair(means, "human_mean", "gpt_mean", "人 vs GPT judge")
    results["human_vs_llm_mean"] = compute_icc_pair(means, "human_mean", "llm_mean", "人 vs LLM 均值")
    results["claude_vs_gpt"] = compute_icc_pair(means, "claude_mean", "gpt_mean", "Claude vs GPT (参照)")

    print("\n=== 结果解读 ===")
    for k, v in results.items():
        print(f"  {k}: ICC(2,1)={v['ICC21']:.3f} → {interpret_icc(v['ICC21'])}")

    # 保存结果
    out = BLIND / "icc_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "n": len(df),
            "per_paper": df.to_dict("records"),
            "icc": {k: {kk: (float(vv) if vv is not None else None) for kk, vv in v.items()} for k, v in results.items()},
        }, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果保存至 {out}")


if __name__ == "__main__":
    main()
