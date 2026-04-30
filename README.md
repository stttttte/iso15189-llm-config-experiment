# ISO 15189 LLM Config Experiment

> **Dataset and code for: "Systematic Divergence Between LLM Judges and Domain Experts in LLM-Assisted ISO 15189:2022 Medical Laboratory Document Generation — A Multi-Level Validation Study"**

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](./LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/data-CC_BY_4.0-lightgrey.svg)](./LICENSE-DATA)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org)

## Overview

This repository accompanies a study on LLM-assisted generation of ISO 15189:2022 Quality Management System (QMS) documents for medical laboratories. It contains:

- **486 generated QMS documents** — Claude Opus 4.6 (405) + GPT-5.4 (81), across 9 configuration groups × 15 task types × 3 repetitions
- **864 LLM-judge evaluations** — Claude & GPT cross-model scoring on 5 CNAS-reviewer dimensions
- **30 expert blind-review ratings** — 10 papers × 3 ISO 15189-qualified raters (1 CNAS senior technologist + 2 certified internal auditors, same laboratory)
- **All analysis code** — auto-scorer, LLM-judge pipelines, 2×2 symmetric analysis, ICC computation
- **Reproducibility artifacts** — full task messages, prompts, configs, rule definitions

## Key Findings

1. **LLM judges disagree with domain experts** (n=3 raters × 10 papers): ICC(3,1) expert panel vs Claude = 0.548 (p=0.04); vs GPT = 0.217 (ns). Inter-rater ICC(2,k) = 0.982 (excellent consensus among 3 experts)
2. **Both LLM judges systematically overrate** by 0.52–0.90 points (on a 0–5 scale)
3. **"Optimal configuration" depends on the evaluator**:
   - LLM-judge view: H4_sop_only (6K tokens) is optimal
   - Expert view: F_template (35K) ≈ H2 ≈ G_template_rules (38K) are optimal (mean 4.06–4.24); H4 ranks second-to-last (3.20)
4. **4-factor orthogonal ablation (LLM layer)**: rules (+0.511***) and skeleton (+0.213) matter; detailed content and examples contribute nothing or are mildly harmful
5. **Token-bulk trap is model-dependent**: C_full (71K) performs acceptably under Claude generation but collapses under GPT-5.4 generation (cross-evaluation 1.40–1.84 vs. 3.22–4.56)
6. **Claude self-preference bias** = +0.464 (8/9 groups positive); **GPT cross-model bias** = −0.472 (8/9 groups negative)

## Repository Structure

```
iso15189-llm-config-experiment/
├── README.md                         # This file (EN + ZH)
├── LICENSE                           # MIT (code)
├── LICENSE-DATA                      # CC BY 4.0 (data, documents)
├── CITATION.cff                      # Citation metadata
├── requirements.txt                  # Python dependencies
├── .gitignore
│
├── docs/
│   ├── DATA_DICTIONARY.md            # Every JSON/MD file explained
│   ├── REPRODUCIBILITY.md            # Step-by-step re-run guide
│   └── TERMINOLOGY.md                # ZH–EN glossary
│
├── code/                             # Analysis scripts (.py)
│   ├── auto_scorer.py                # Python auto-scorer
│   ├── prepare_*.py                  # Config preparation scripts
│   ├── gpt_generate.py               # GPT-5.4 generation
│   ├── gpt_cnas_judge.py             # GPT judge
│   └── compute_icc.py                # Expert vs LLM ICC analysis
│
├── configs/                          # Configuration group definitions
│   ├── rules.md                      # Expert-reviewed rules layer (3.1K)
│   ├── task_messages/                # 15 task prompts
│   └── per_reference_graph.json
│
├── data/
│   ├── generated/                    # 486 generated QMS documents (Chinese)
│   │   ├── A_bare/ ... H4_sop_only/
│   │   └── gpt4o_*/                # legacy prefix from earlier scripting; actual runtime model = GPT-5.4 (see manuscript §2.2)
│   ├── scores/
│   │   ├── all_scores_*.json         # Auto-scorer outputs
│   │   ├── cnas_judge_final_15tasks.json
│   │   ├── gpt_judge_summary.json
│   │   ├── h_claude_judge_supplement.json
│   │   └── gpt_judge_scores/         # Per-file GPT scores
│   ├── analysis/
│   │   ├── 2x2_symmetric_complete.json
│   │   ├── final_9groups_ranking.json
│   │   ├── ablation_h2h3_results.json
│   │   └── dual_judge_comparison.json
│   └── expert_blind_review/
│       ├── papers/                         # paper_01–10 (anonymized)
│       ├── rating_sheet_rater1_filled.md   # Rater 1 (CNAS senior tech) scores
│       ├── rating_sheet_rater2_filled.md   # Rater 2 (internal auditor) scores
│       ├── rating_sheet_rater3_filled.md   # Rater 3 (internal auditor) scores
│       ├── icc_results.json                # Single-rater ICC (legacy)
│       └── icc_results_3raters.json        # 3-rater ICC analysis
│
├── figures/                          # Publication figures (PNG 300 DPI + SVG)
│   ├── fig1_config_composition.*     # 9 configurations × 4 components
│   ├── fig2_2x2_symmetric.*          # 2×2 cross-model validation heatmap
│   ├── fig3_expert_vs_llm.*          # Expert panel vs LLM judge scatter
│   └── fig4_token_vs_quality.*       # Token size vs quality dual-perspective
│
└── paper/
    └── outline_v16_zh.md             # Paper outline (Chinese)
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/stttttte/iso15189-llm-config-experiment.git
cd iso15189-llm-config-experiment

# 2. Install dependencies
pip install -r requirements.txt

# 3. Reproduce key analyses (no API calls needed)
python3 code/compute_icc_3raters.py          # 3-rater expert panel vs LLM ICC (primary)
python3 code/compute_icc.py                  # Single-rater ICC (legacy)
python3 -c "
from pathlib import Path
import json
d = json.load(open('data/analysis/final_9groups_ranking.json'))
print(json.dumps(d['ranking'], ensure_ascii=False, indent=2))
"

# 4. Re-run LLM generation / judging (requires API keys)
export GPT_API_KEY='your-key-here'
python3 code/gpt_generate.py --tasks A1,B1,C1 --model gpt-5.4
python3 code/gpt_cnas_judge.py --all --model gpt-5.4
```

Full reproducibility guide: [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md)

## Language Note

**Generated QMS documents are in Chinese** — this is by design, as the research subject is Chinese-language ISO 15189 implementation per CNAS-CL02:2023 (the Chinese accreditation criterion). English translations of representative excerpts appear in the paper; the Chinese originals are preserved here as scientific research objects. See [`docs/TERMINOLOGY.md`](docs/TERMINOLOGY.md) for an EN–ZH glossary.

**All analysis code, file names, variable names, and documentation are in English.**

## Citation

If you use this dataset or code, please cite both:

1. The paper (preprint DOI to be added upon preprint submission):
   ```
   [authors] (2026). Systematic Divergence Between LLM Judges and Domain Experts
   in LLM-Assisted ISO 15189:2022 Medical Laboratory Document Generation:
   A Multi-Level Validation Study. [journal / preprint venue].
   ```

2. This repository:
   See [`CITATION.cff`](CITATION.cff) or use GitHub's "Cite this repository" button.

## License

- **Code** (`.py`, `.sh`): [MIT License](LICENSE)
- **Data and documents** (`.md`, `.json`, generated QMS files): [CC BY 4.0](LICENSE-DATA)

In short: use freely with attribution.

## Ethical Considerations

- **No Protected Health Information (PHI)**: All 486 generated documents use placeholder names (e.g., "李某", "张医生") and generic institution types (e.g., "妇幼保健院") with no identifiable individuals or facilities.
- **No API keys committed**: all LLM-API scripts read keys via environment variables.
- **Expert blind review**: The key mapping (which paper came from which configuration group) is stored in `blind_review/key.json` and is **intentionally excluded** from this release to preserve blind-review integrity for future third-party validation studies. The 3 raters' filled scoring sheets (rater1/2/3) are released to enable third-party re-analysis.
- **Rater informed consent**: Raters 2 and 3 provided informed consent prior to scoring. Their names and ID numbers are stripped from the released files; only role labels (e.g., "Rater 2, internal auditor") are retained.

## Acknowledgments

- Claude Opus 4.6 (Anthropic) — primary generation model + judge
- GPT-5.4 (OpenAI, via AIHubMix) — cross-model validation generation + judge
- CNAS-qualified senior laboratory technologist — expert blind reviewer
- `pingouin` (Vallat, 2018) — ICC computation

---

## 中文摘要

本仓库为一项针对 LLM 辅助 ISO 15189:2022 医学实验室质量管理体系（QMS）文件生成的研究提供数据和代码。

### 核心内容

- **486 篇生成的 QMS 中文文件**：Claude Opus 4.6（405 篇）+ GPT-5.4（81 篇），覆盖 9 组配置 × 15 任务类型 × 3 重复
- **864 次 LLM 评审评分**：Claude 与 GPT 跨模型评估，5 维度 CNAS 评审员视角
- **30 次专家盲评**：10 篇 × 3 位 ISO 15189 资格专家（1 位 CNAS 主任技师 + 2 位同单位合格内审员），专家间 ICC(2,k)=0.982
- **完整分析代码**：自动评分器、LLM 判官流水线、2×2 对称分析、ICC 计算
- **可复现材料**：任务 prompt、配置模板、规则定义等

### 核心发现

1. LLM 评审与领域专家评估存在系统性分歧（n=3 rater，ICC(3,1) 专家均值 vs Claude = 0.548, p=0.04; vs GPT = 0.217, ns）
2. 两个 LLM 判官系统性高估 0.55–0.93 分
3. 配置的"最优性"取决于评估者：LLM 视角 H4 (6K) 最优；专家视角 F/G/H2 (35–61K) 最优（专家均值 4.06–4.24），**H4 在专家视角倒数第二**（3.20）
4. 4 因子正交消融（LLM 层）：规则层和骨架层有效；详细内容无贡献；示例轻微有害
5. token 体量陷阱的模型依赖性：C_full (71K) 在 Claude 下勉强可用，在 GPT 下完全崩盘
6. Claude 自评偏见 +0.464；GPT 反向偏见 −0.472

### 使用与引用

- 详见英文部分
- 投稿正文为英文；本仓库的所有中文 QMS 生成文件是研究对象本身，故保留原文
- 代码采用 MIT 许可；数据采用 CC BY 4.0 许可
