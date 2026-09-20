"""Reproduce the four final CCLM figure forms from released local data.

Run from any working directory:
    python code/make_figures.py
    python code/make_figures.py --output-dir /path/to/output

Writes Figure1–4 as PNG (300 dpi) and SVG under reproduced/figures by default.
Preserves the archived figures and input data. No API calls or network access.
The figures retain the final v4 forms; Figures 1 and 4 use explicitly described
archived configuration sizes. Figure 4b uses the automated/GPT composite ranking,
restricted to the seven expert-reviewed configurations.
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reproduced" / "figures"

INK, INK2, SURFACE = "#1F2429", "#5A6570", "#FFFFFF"
BLUE, GREEN, VERM, PINK = "#0072B2", "#009E73", "#D55E00", "#CC79A7"
SEQ_LO, SEQ_HI = "#F2F7FC", "#08519C"

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 10,
    "axes.linewidth": 0.7, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK,
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.fontsize": 8.5, "legend.frameon": False,
    "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight",
    "savefig.facecolor": SURFACE, "figure.facecolor": SURFACE,
})

# Archived configuration size, in thousands of cl100k_base tokens.
# These are descriptive sizes of the released configuration artifacts, NOT
# reconstructed Claude invocation inputs, API token usage, or cost thresholds.
# F/G/H2/H3/H4: mean across configs/per_task_assembled/{prefix}_{task}.txt,
# 15 tasks each, rounded to the nearest token. Fixed artifacts:
# B: code/gpt_generate.py::load_simple_prompt() literal;
# E: configs/rules.md; C: configs/full_config.txt. A is the empty configuration.
ARCHIVED_TOKEN_K = {
    "A_bare": 0.0, "B_simple": 0.348, "E_rules": 1.236,
    "E_rules_v2": 1.236, "H4_sop_only": 2.373, "H3_skeleton": 5.375,
    "F_template": 23.090, "G_template_rules": 24.235,
    "H2_keep_examples": 25.052, "C_full": 56.151,
}
# (configuration, rules, skeleton, detailed content, examples)
COMPONENTS = [
    ("A_bare", 0, 0, 0, 0), ("B_simple", 0.5, 0, 0, 0),
    ("E_rules", 1, 0, 0, 0), ("H4_sop_only", 1, 0.5, 0, 0),
    ("H3_skeleton", 1, 1, 0, 0), ("F_template", 0, 1, 1, 0),
    ("G_template_rules", 1, 1, 1, 0), ("H2_keep_examples", 1, 1, 1, 1),
    ("C_full", 0.5, 1, 1, 1),
]
GROUPS = sorted(
    [(g, ARCHIVED_TOKEN_K[g], *components) for g, *components in COMPONENTS],
    key=lambda row: row[1],
)
SHORT = {"A_bare": "A", "B_simple": "B", "E_rules": "E", "E_rules_v2": "E",
         "H4_sop_only": "H4", "H3_skeleton": "H3", "F_template": "F",
         "G_template_rules": "G", "H2_keep_examples": "H2", "C_full": "C"}
FAMILY = {"A_bare": "base", "B_simple": "min", "E_rules": "min", "E_rules_v2": "min",
          "H4_sop_only": "min", "H3_skeleton": "min", "F_template": "tpl",
          "G_template_rules": "tpl", "H2_keep_examples": "tpl", "C_full": "full"}
FAMC = {"min": BLUE, "tpl": GREEN, "full": VERM}


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=300)
    fig.savefig(OUT / f"{name}.svg")
    plt.close(fig)
    print(f"{name}.png + {name}.svg")


def load_fig2():
    with (ROOT / "data" / "analysis" / "2x2_symmetric_complete.json").open(encoding="utf-8") as handle:
        data = json.load(handle)["matrix"]
    order = [g[0] for g in GROUPS]
    quads = ["CC", "CG", "GC", "GG"]
    mat = np.zeros((9, 4))
    for i, g in enumerate(order):
        src = {"E_rules": "E_rules_v2"}.get(g, g)
        for j, q in enumerate(quads):
            mat[i, j] = data[src][q]
    return order, mat


def load_fig3():
    with (ROOT / "data" / "expert_blind_review" / "icc_results_3raters.json").open(encoding="utf-8") as handle:
        d = json.load(handle)
    return d["per_paper"], d["icc"]


def load_fig4():
    papers, _ = load_fig3()
    by = pd.DataFrame(papers).groupby("group").agg(
        expert=("expert_mean", "mean"),
        claude=("claude_mean", "mean"),
        gpt=("gpt_mean", "mean"),
    ).reset_index()
    by["tokens"] = by["group"].map(ARCHIVED_TOKEN_K)
    if by["tokens"].isna().any():
        raise ValueError("An expert-reviewed configuration lacks archived token metadata")
    return by.sort_values("tokens")


def load_composite_ranking(groups):
    """Table 1 automated/GPT composite; ignore the historical token field."""
    with (ROOT / "data" / "analysis" / "final_9groups_ranking.json").open() as handle:
        rows = json.load(handle)["ranking"]
    result = [row[0] for row in sorted(rows, key=lambda row: row[1], reverse=True)
              if row[0] in groups]
    if len(result) != len(set(result)) or set(result) != set(groups):
        raise ValueError("Composite ranking must cover each expert-reviewed configuration once")
    return result


def figure1():  # single panel: matrix + inline token bars
    comps = ["Rules", "Skeleton", "Detailed\ncontent", "Examples"]
    names = [g[0].replace("_", " ") for g in GROUPS]
    matrix = np.array([g[2:] for g in GROUPS], float)
    toks = np.array([g[1] for g in GROUPS])
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    mid = LinearSegmentedColormap.from_list("m", [SEQ_LO, SEQ_HI])(0.45)
    cmap = ListedColormap(["#F4F4F2", mid, SEQ_HI])
    ax.pcolormesh(np.arange(5), np.arange(10), np.digitize(matrix, [0.25, 0.75]),
                  cmap=cmap, edgecolors=SURFACE, linewidth=2, vmin=0, vmax=2)
    for i in range(9):
        for j in range(4):
            v = matrix[i, j]
            sym = "✓" if v == 1 else ("◑" if v == 0.5 else "—")
            col = "white" if v == 1 else (INK if v == 0.5 else "#B8B8B4")
            ax.text(j + 0.5, i + 0.5, sym, ha="center", va="center",
                    fontsize=10, color=col, fontweight="bold" if v else "normal")
    # inline token bars in an appended column region
    x0, xmax_bar = 4.35, 7.6
    scale = (xmax_bar - x0) / max(toks)
    bar_col = LinearSegmentedColormap.from_list("m", [SEQ_LO, SEQ_HI])(0.78)
    for i, v in enumerate(toks):
        ax.add_patch(mpatches.Rectangle((x0, i + 0.22), v * scale, 0.56,
                                        fc=bar_col, ec="none"))
        lab = "0" if v == 0 else (f"{v:.3f}K" if v < 1 else f"{v:.1f}K")
        ax.text(x0 + v * scale + 0.06, i + 0.5, lab, va="center", fontsize=8, color=INK)
    ax.text((x0 + xmax_bar) / 2 - 0.1, 9.55, "Archived configuration size\n(cl100k_base tokens)",
            ha="center", fontsize=8.5, color=INK)
    for j, c in enumerate(comps):
        ax.text(j + 0.5, 9.55, c, ha="center", fontsize=8.5, color=INK)
    ax.set_yticks(np.arange(9) + 0.5)
    ax.set_yticklabels(names, fontsize=8.5)
    ax.set_xticks([])
    ax.set_xlim(0, 8.6); ax.set_ylim(0, 10.2)
    ax.tick_params(length=0)
    [sp.set_visible(False) for sp in ax.spines.values()]
    handles = [mpatches.Patch(fc=SEQ_HI, label="included"),
               mpatches.Patch(fc=mid, label="partial"),
               mpatches.Patch(fc="#F4F4F2", ec="#DDDDD8", label="absent")]
    ax.legend(handles=handles, ncol=3, loc="upper left",
              bbox_to_anchor=(0.0, -0.01), handlelength=1.1, columnspacing=1.2)
    save(fig, "Figure1")

def figure2():  # dumbbell + value labels on C_full row
    order, mat = load_fig2()
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    d = 0.16
    for i, g in enumerate(order):
        cc, cg, gc, gg = mat[i]
        ax.plot([min(cc, cg), max(cc, cg)], [i + d] * 2, color=BLUE, lw=2, alpha=0.55)
        ax.plot(cc, i + d, "o", ms=6, color=BLUE)
        ax.plot(cg, i + d, "^", ms=6, color=BLUE)
        ax.plot([min(gc, gg), max(gc, gg)], [i - d] * 2, color=VERM, lw=2, alpha=0.55)
        ax.plot(gc, i - d, "o", ms=6, color=VERM)
        ax.plot(gg, i - d, "^", ms=6, color=VERM)
    ci = order.index("C_full")
    ax.axhspan(ci - 0.44, ci + 0.44, color=VERM, alpha=0.07, lw=0)
    cc, cg, gc, gg = mat[ci]
    ax.annotate(f"{gc:.2f}", (gc, ci - d), xytext=(-2, -11), textcoords="offset points",
                fontsize=7.5, color=VERM, ha="center", fontweight="bold")
    ax.annotate(f"{gg:.2f}", (gg, ci - d), xytext=(2, -11), textcoords="offset points",
                fontsize=7.5, color=VERM, ha="center", fontweight="bold")
    ax.annotate(f"{cg:.2f}", (cg, ci + d), xytext=(0, 8), textcoords="offset points",
                fontsize=7.5, color=BLUE, ha="center")
    ax.annotate(f"{cc:.2f}", (cc, ci + d), xytext=(0, 8), textcoords="offset points",
                fontsize=7.5, color=BLUE, ha="center")
    ax.text(1.62, ci - 0.95, "collapse: GPT-generated C_full",
            fontsize=8, color=VERM, fontweight="bold", ha="left")
    ax.set_yticks(np.arange(9))
    ax.set_yticklabels([g.replace("_", " ") for g in order], fontsize=8.5)
    ax.set_ylim(-0.65, 8.95)
    ax.set_xlim(1.0, 5.1)
    ax.set_xlabel("Mean judge score (0–5)")
    ax.grid(axis="x", alpha=0.18, lw=0.6)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    handles = [
        plt.Line2D([], [], color=BLUE, lw=2.4, label="Claude-generated"),
        plt.Line2D([], [], color=VERM, lw=2.4, label="GPT-generated"),
        plt.Line2D([], [], marker="o", ls="", color=INK2, ms=6, label="Claude judge"),
        plt.Line2D([], [], marker="^", ls="", color=INK2, ms=6, label="GPT judge"),
    ]
    ax.legend(handles=handles, ncol=4, loc="upper left",
              bbox_to_anchor=(-0.02, -0.13), columnspacing=1.2, handletextpad=0.5)
    save(fig, "Figure2")


def figure3():  # Bland-Altman with in-panel labels
    papers, icc = load_fig3()
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.9), sharey=True, sharex=True)
    for k, (ax, (jn, col, key)) in enumerate(zip(
            axes, [("Claude Opus 4.6 judge", "claude_mean", "expert_vs_claude"),
                   ("GPT-5.4 judge", "gpt_mean", "expert_vs_gpt")])):
        e = np.array([p["expert_mean"] for p in papers])
        j = np.array([p[col] for p in papers])
        m, d_ = (e + j) / 2, j - e
        md, sd = d_.mean(), d_.std(ddof=1)
        lo, hiL = md - 1.96 * sd, md + 1.96 * sd
        ax.axhline(0, color=INK, lw=0.9)
        ax.axhspan(lo, hiL, color=VERM, alpha=0.05, lw=0)
        ax.axhline(md, color=VERM, lw=1.5)
        for lim in (hiL, lo):
            ax.axhline(lim, color=VERM, lw=0.9, ls=(0, (4, 3)), alpha=0.8)
        for p, x, y in zip(papers, m, d_):
            fam = FAMILY[p["group"]]
            if fam == "base":
                ax.scatter(x, y, s=48, fc="white", ec=INK, lw=1.1, zorder=4)
            else:
                ax.scatter(x, y, s=48, fc=FAMC[fam], ec="white", lw=0.9, zorder=4)
        ax.text(0.98, (md - (-1.0)) / 3.3 + 0.035, f"bias {md:+.2f}",
                transform=ax.transAxes, fontsize=8, color=VERM,
                ha="right", fontweight="bold")
        ax.text(0.98, (hiL - (-1.0)) / 3.3 + 0.03, "+1.96 SD",
                transform=ax.transAxes, fontsize=6.8, color=VERM, ha="right")
        ax.text(0.98, (lo - (-1.0)) / 3.3 - 0.075, "−1.96 SD",
                transform=ax.transAxes, fontsize=6.8, color=VERM, ha="right")
        ax.set_xlim(3.1, 4.6)
        ax.set_ylim(-1.0, 2.3)
        ax.set_xlabel("Mean of expert and judge")
        ax.set_title(jn, loc="left", fontsize=9, pad=8)
        ax.text(-0.05, 1.06, "ab"[k], transform=ax.transAxes, fontsize=12,
                fontweight="bold", va="bottom")
    axes[0].set_ylabel("Judge − expert (points)")
    axes[0].text(3.13, -0.09, "0 = perfect agreement", fontsize=7,
                 color=INK2, va="top")
    handles = [
        plt.Line2D([], [], marker="o", ls="", mfc=FAMC["min"], mec="white", ms=7,
                   label="Minimal (rules/skeleton)"),
        plt.Line2D([], [], marker="o", ls="", mfc=FAMC["tpl"], mec="white", ms=7,
                   label="Template-anchored"),
        plt.Line2D([], [], marker="o", ls="", mfc=FAMC["full"], mec="white", ms=7,
                   label="Full-context"),
        plt.Line2D([], [], marker="o", ls="", mfc="white", mec=INK, ms=7,
                   label="No-prompt baseline"),
    ]
    fig.legend(handles=handles, ncol=4, loc="lower center",
               bbox_to_anchor=(0.5, -0.05), columnspacing=1.3, handletextpad=0.4)
    fig.subplots_adjust(wspace=0.08, bottom=0.22)
    save(fig, "Figure3")


def figure4():  # composite: a) three lines  b) rank bump
    by = load_fig4()
    fig, (ax, axb) = plt.subplots(1, 2, figsize=(9.6, 4.3),
                                  gridspec_kw={"width_ratios": [1.55, 1], "wspace": 0.24})
    # -- a: lines
    ax.plot(by["tokens"], by["claude"], marker="o", ms=5, lw=1.4, color=VERM)
    ax.plot(by["tokens"], by["gpt"], marker="^", ms=5, lw=1.4, color=BLUE)
    ax.plot(by["tokens"], by["expert"], marker="s", ms=6, lw=2.5, color=GREEN)
    for lab, (c, colname) in {"Claude judge": (VERM, "claude"),
                              "GPT judge": (BLUE, "gpt"),
                              "Expert": (GREEN, "expert")}.items():
        y = by.loc[by.group == "C_full", colname].iloc[0]
        ax.annotate(lab, (ARCHIVED_TOKEN_K["C_full"], y), xytext=(6, 0), textcoords="offset points",
                    fontsize=7.8, color=c, va="center", fontweight="bold")
    off = {"A_bare": (0, -13), "E_rules_v2": (-4, -13), "H4_sop_only": (7, -13),
           "F_template": (-11, 3), "G_template_rules": (4, -14),
           "H2_keep_examples": (3, 8), "C_full": (0, -14)}
    for _, r in by.iterrows():
        dx, dy = off.get(r["group"], (0, -12))
        ax.annotate(SHORT.get(r["group"], r["group"]), (r["tokens"], r["expert"]),
                    xytext=(dx, dy), textcoords="offset points",
                    fontsize=7.2, color=INK, ha="center")
    ax.set_xscale("symlog", linthresh=0.5)
    ax.set_xticks([0, 1, 2, 5, 25, 56])
    ax.set_xticklabels(["0", "1K", "2K", "5K", "25K", "56K"])
    ax.set_xlim(-0.18, 340)
    ax.set_ylim(2.8, 5.35)
    ax.set_yticks([3, 3.5, 4, 4.5, 5])
    ax.set_xlabel("Archived configuration size\n(cl100k_base tokens, symlog)")
    ax.set_ylabel("Mean quality score (0–5)")
    ax.grid(axis="y", alpha=0.18, lw=0.6)
    ax.set_axisbelow(True)
    ax.text(-0.1, 1.05, "a", transform=ax.transAxes, fontsize=12,
            fontweight="bold", va="bottom")

    # -- b: bump
    llm_rank = load_composite_ranking(set(by["group"]))
    exp_rank = list(by.sort_values("expert", ascending=False)["group"])
    focus = {"H4_sop_only": VERM, "F_template": GREEN}
    for g in llm_rank:
        r0, r1 = llm_rank.index(g) + 1, exp_rank.index(g) + 1
        c = focus.get(g, "#C2CAD1")
        lw = 2.6 if g in focus else 1.3
        axb.plot([0, 1], [r0, r1], color=c, lw=lw, zorder=3 if g in focus else 2)
        axb.plot(0, r0, "o", ms=6.5, color=c, zorder=4)
        axb.plot(1, r1, "o", ms=6.5, color=c, zorder=4)
        axb.annotate(g.replace("_", " "), (0, r0), xytext=(-9, 0),
                     textcoords="offset points", ha="right", va="center",
                     fontsize=7.8, color=INK if g in focus else INK2,
                     fontweight="bold" if g in focus else "normal")
    axb.annotate("#1 → #5", (1, 5), xytext=(10, 0), textcoords="offset points",
                 fontsize=8, color=VERM, fontweight="bold", va="center")
    axb.annotate("#6 → #1", (1, 1), xytext=(10, 0), textcoords="offset points",
                 fontsize=8, color=GREEN, fontweight="bold", va="center")
    axb.set_xlim(-0.95, 1.42)
    axb.set_ylim(7.6, 0.4)
    axb.set_xticks([0, 1])
    axb.set_xticklabels(["Automated/GPT\ncomposite", "Expert panel"], fontsize=8.5)
    axb.set_yticks(range(1, 8))
    axb.set_yticklabels([f"#{i}" for i in range(1, 8)], fontsize=7.5)
    axb.tick_params(length=0)
    [sp.set_visible(False) for sp in axb.spines.values()]
    axb.text(-0.32, 1.05, "b", transform=axb.transAxes, fontsize=12,
             fontweight="bold", va="bottom")
    axb.set_title("Configuration ranking", loc="left", fontsize=9, pad=8)
    save(fig, "Figure4")


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT,
                        help="Output directory (default: repository/reproduced/figures)")
    OUT = parser.parse_args().output_dir.resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    figure1()
    figure2()
    figure3()
    figure4()


if __name__ == "__main__":
    main()
