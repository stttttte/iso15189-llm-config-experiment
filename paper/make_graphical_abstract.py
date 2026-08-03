"""CCLM 图形摘要：LLM 评判者与专家的排名反转。

形式选择：数据的任务是"一个头条结论"——同一批配置，换个评审者排名就翻转。
bump chart 是唯一能让"交叉"本身承载信息的形式；配色沿用正文四图（Okabe-Ito 子集，验证全过）。
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from pathlib import Path

BASE = Path(__file__).resolve().parent

BLUE, GREEN, VERM = "#0072B2", "#009E73", "#D55E00"
INK, INK2, MUTED = "#1F2429", "#5A6570", "#9AA3AB"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "axes.linewidth": 0,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})

# 左：LLM 评判者综合排名（7 个受专家评审的配置）；右：专家排名
LLM_RANK = ["H4_sop_only", "G_template_rules", "H2_keep_examples",
            "E_rules_v2", "C_full", "F_template", "A_bare"]
EXPERT_RANK = ["F_template", "H2_keep_examples", "G_template_rules",
               "C_full", "H4_sop_only", "E_rules_v2", "A_bare"]
EXPERT_SCORE = {"F_template": 4.24, "H2_keep_examples": 4.07, "G_template_rules": 4.06,
                "C_full": 3.45, "H4_sop_only": 3.20, "E_rules_v2": 3.19, "A_bare": 3.04}

FOCUS = {"H4_sop_only": VERM, "F_template": GREEN}
LABEL = {"H4_sop_only": "H4_sop_only\n(minimal, ~2k tokens)",
         "F_template": "F_template\n(template, ~15k tokens)"}


def curve(ax, x0, y0, x1, y1, color, lw, alpha=1.0, z=3):
    """S 形连线：两端水平，避免直线交叉处的视觉噪声。"""
    dx = (x1 - x0) * 0.42
    p = MPath([(x0, y0), (x0 + dx, y0), (x1 - dx, y1), (x1, y1)],
              [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
    ax.add_patch(PathPatch(p, fc="none", ec=color, lw=lw, alpha=alpha,
                           zorder=z, capstyle="round"))


def build():
    fig = plt.figure(figsize=(9.0, 5.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # ---- 标题区 ----
    ax.text(0.42, 5.62, "The best prompt depends on who grades it",
            fontsize=17, fontweight="bold", color=INK, va="top")
    ax.text(0.42, 5.16,
            "486 ISO 15189 quality management documents drafted by two LLMs under nine prompt configurations,\n"
            "then scored by LLM judges and, blinded, by three qualified internal auditors.",
            fontsize=8.6, color=INK2, va="top", linespacing=1.5)

    # ---- bump 图区 ----
    xl, xr = 3.05, 6.35
    top, step = 4.05, 0.42

    def ypos(rank):
        return top - (rank - 1) * step

    ax.text(xl, top + 0.42, "LLM judges", fontsize=10.5, fontweight="bold",
            color=INK, ha="right")
    ax.text(xr, top + 0.42, "Human experts", fontsize=10.5, fontweight="bold",
            color=INK, ha="left")
    ax.plot([xl, xl], [ypos(7) - 0.2, top + 0.26], color=MUTED, lw=0.8, alpha=0.5)
    ax.plot([xr, xr], [ypos(7) - 0.2, top + 0.26], color=MUTED, lw=0.8, alpha=0.5)

    for cfg in LLM_RANK:
        r0 = LLM_RANK.index(cfg) + 1
        r1 = EXPERT_RANK.index(cfg) + 1
        focus = cfg in FOCUS
        col = FOCUS.get(cfg, MUTED)
        curve(ax, xl, ypos(r0), xr, ypos(r1), col,
              lw=2.6 if focus else 1.2, alpha=1.0 if focus else 0.45,
              z=5 if focus else 3)
        for x, r, ha in ((xl, r0, "right"), (xr, r1, "left")):
            ax.scatter(x, ypos(r), s=132 if focus else 74, zorder=6,
                       fc=col if focus else "white",
                       ec=col if focus else MUTED, lw=1.6 if focus else 1.1)
            ax.text(x, ypos(r), str(r), fontsize=8.2 if focus else 7.4,
                    fontweight="bold", ha="center", va="center", zorder=7,
                    color="white" if focus else INK2)

    # 焦点标注
    ax.text(xl - 0.34, ypos(1), LABEL["H4_sop_only"], fontsize=8.4, ha="right",
            va="center", color=VERM, fontweight="bold", linespacing=1.45)
    ax.text(xl - 0.34, ypos(6), LABEL["F_template"], fontsize=8.4, ha="right",
            va="center", color=GREEN, fontweight="bold", linespacing=1.45)
    ax.text(xr + 0.30, ypos(5), "fell to 5th\n(3.20 / 5)", fontsize=8.4, ha="left",
            va="center", color=VERM, fontweight="bold", linespacing=1.45)
    ax.text(xr + 0.30, ypos(1), "rose to 1st\n(4.24 / 5)", fontsize=8.4, ha="left",
            va="center", color=GREEN, fontweight="bold", linespacing=1.45)

    # 其余配置的浅灰标签（右侧，按专家排名）
    for cfg in EXPERT_RANK:
        if cfg in FOCUS:
            continue
        r1 = EXPERT_RANK.index(cfg) + 1
        ax.text(xr + 0.30, ypos(r1), cfg, fontsize=7.6, ha="left", va="center",
                color=MUTED)

    # ---- 底部结论条 ----
    y0 = 0.30
    ax.plot([0.42, 9.58], [y0 + 0.86, y0 + 0.86], color="#E3E6E8", lw=1.2)
    facts = [
        (VERM, "LLM judges overrate", "compliance by 0.52–0.90 points"),
        (BLUE, "Only rules mattered", "of four prompt components (Δ = 0.51)"),
        (GREEN, "Expert review", "remains indispensable"),
    ]
    for i, (col, head, tail) in enumerate(facts):
        x = 0.42 + i * 3.16
        ax.add_patch(plt.Rectangle((x, y0 + 0.14), 0.075, 0.42, fc=col, ec="none"))
        ax.text(x + 0.22, y0 + 0.44, head, fontsize=9.2, fontweight="bold",
                color=INK, va="center")
        ax.text(x + 0.22, y0 + 0.17, tail, fontsize=8.2, color=INK2, va="center")

    return fig


if __name__ == "__main__":
    fig = build()
    out_png = BASE / "figures" / "graphical_abstract.png"
    out_svg = BASE / "figures" / "graphical_abstract.svg"
    fig.savefig(out_png, dpi=300, bbox_inches="tight", pad_inches=0.16)
    fig.savefig(out_svg, bbox_inches="tight", pad_inches=0.16)
    print(f"saved {out_png}")
