# ISO 15189 LLM Config Experiment

> **Dataset and code for: "Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents: Prompt Configuration, LLM-as-Judge Bias, and Exploratory Expert Validation"**

Release **v1.2.0** contains the author-approved reporting and reproducibility corrections dated 20 September 2026 and is archived on [Zenodo, DOI: 10.5281/zenodo.22855972](https://doi.org/10.5281/zenodo.22855972). See the [release notes](docs/RELEASE_NOTES_v1.2.0.md). The main-branch manuscript and cover letter include a post-release citation-only update to this newly assigned DOI; research data and analyses are unchanged. The [v1.1.0 archive](https://doi.org/10.5281/zenodo.21769007) remains a historical release.

The current manuscript is `paper/CCA_manuscript_consistency_revised.md` (with a matching Word file). Earlier `paper/manuscript_v2_en_CCLM.*` and `Liu_2026_CCLM_*` submission files remain historical records; their wording and numerical claims are not the corrected version.

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](./LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/data-CC_BY_4.0-lightgrey.svg)](./LICENSE-DATA)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org)

## Overview

This repository accompanies a study on LLM-assisted generation of ISO 15189:2022 Quality Management System (QMS) documents for medical laboratories. It contains:

- **486 generated QMS documents** — 405 Claude Opus 4.6 documents (9 groups × 15 tasks × 3 repetitions) and 81 GPT-5.4 documents (9 groups × tasks A1/B1/C1 × 3 repetitions).
- **759 archived document-level judge records** — 486 GPT-judge records and 273 Claude-judge records. Additional historical Claude group means survive in the 2×2 summary, without enough raw records to reconstruct their denominators.
- **30 expert rating forms** — 10 Claude-generated Class A documents × 3 same-institution coauthor raters (1 senior laboratory technologist and 2 internal auditors).
- **Offline reproduction scripts** — three-rater ICC, nine-group composite ranking, component contrasts, and figures; historical generation/judging scripts are also retained.
- **Archived task messages and configurations** — configuration-text token counts are documented separately from actual model input usage, which cannot be verified for Claude.

## Key Findings

1. **Exploratory expert comparison:** ICC(3,1) between the three-rater expert mean and Claude = 0.548; with GPT = 0.217. Expert inter-rater ICC(2,k) = 0.982. These estimates come from only 10 documents.
2. **Mean LLM overrating:** Claude +0.90 and GPT +0.52 points relative to the expert mean, on a 0–5 scale.
3. **Rankings depend on the evaluation method:** H4 leads the nine-group composite of auto-scores and GPT-judge scores. In the expert subset, F/H2/G have the highest descriptive means (4.06–4.24); H4 scores 3.20 and ranks fifth of seven represented groups. Unequal, small group samples do not establish an optimal configuration.
4. **Structured component contrasts:** rules Δ=+0.511 (Benjamini–Hochberg adjusted p=0.000562); skeleton Δ=+0.213 (adjusted p=0.109, not significant). The design is not a Taguchi orthogonal array, and nonsignificant detail/example contrasts do not establish no effect.
5. **Model-dependent results:** in the historical 2×2 summary, C_full scores 1.40–1.84 for GPT-generated documents and 3.22–4.56 for Claude-generated documents. This comparison does not establish a token threshold or equivalent model inputs.
6. **Two distinct bias contrasts:** within-judge generator contrasts are +0.294 for Claude and −0.301 for GPT. Same-generator, between-judge sensitivity contrasts are +0.464 and −0.472, respectively. See the [data dictionary](docs/DATA_DICTIONARY.md#3-analysis-outputs) for formulas and archive limitations.

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
│   ├── DATA_DICTIONARY.md            # Principal data schemas and limits
│   ├── REPRODUCIBILITY.md            # Step-by-step re-run guide
│   └── TERMINOLOGY.md                # ZH–EN glossary
│
├── code/                             # Analysis scripts (.py)
│   ├── auto_scorer.py                # Python auto-scorer
│   ├── prepare_*.py                  # Config preparation scripts
│   ├── gpt_generate.py               # GPT-5.4 generation
│   ├── gpt_cnas_judge.py             # GPT judge
│   ├── compute_icc_3raters.py        # Primary expert-panel ICC reproduction
│   ├── reproduce_ranking.py         # Recompute Table 1 composite ranking
│   ├── bootstrap_ci.py              # Component-contrast intervals
│   └── make_figures.py              # Corrected figure reproduction
│
├── configs/                          # Configuration group definitions
│   ├── rules.md                      # Archived rules text (1,236 cl100k_base tokens)
│   ├── per_task_assembled/           # F/G/H2/H3/H4 text for all 15 tasks
│   ├── task_messages/                # 15 task prompts
│   └── full_config.txt               # Archived full configuration
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
│   │   ├── configuration_token_inventory.json
│   │   ├── ablation_h2h3_results.json
│   │   └── dual_judge_comparison.json
│   └── expert_blind_review/
│       ├── papers/                         # paper_01–10 (anonymized)
│       ├── rating_sheet_rater1_filled.md   # Rater 1 (CNAS senior tech) scores
│       ├── rating_sheet_rater2_filled.md   # Rater 2 (internal auditor) scores
│       ├── rating_sheet_rater3_filled.md   # Rater 3 (internal auditor) scores
│       ├── blind_key.json                  # Mapping recoverable from released results
│       ├── icc_results.json                # Single-rater ICC (legacy)
│       └── icc_results_3raters.json        # 3-rater ICC analysis
│
├── figures/                          # Historical figure files retained
├── reproduced/                       # New offline outputs (created by scripts)
│   └── figures/                      # Configuration size, judge contrasts,
│                                     # Bland–Altman, and score/rank comparisons
│
└── paper/
    ├── CCA_manuscript_consistency_revised.md
    ├── CCA_manuscript_consistency_revised.docx
    └── ...                           # Earlier manuscript versions retained
```

## Quick Start

```bash
# 1. Open the root of this corrected working copy.

# The public repository/archive does not yet contain these corrections.

# 2. Install dependencies

pip install -r requirements.txt

# 3. Reproduce key analyses (no API calls needed)

python3 code/compute_icc_3raters.py
python3 code/reproduce_ranking.py
python3 code/bootstrap_ci.py
python3 code/make_figures.py
```

File outputs are written under `reproduced/`; archived scores remain unchanged. The bootstrap script prints its results. New generation is a separate workflow: the legacy scripts need path adaptation, API credentials, and any required licensed source templates. They are not ready to run unchanged from a fresh checkout.

Full reproducibility guide: [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md)

## Language Note

**Generated QMS documents are in Chinese** — this is by design, as the research subject is Chinese-language ISO 15189 implementation per CNAS-CL02:2023 (the Chinese accreditation criterion). English translations of representative excerpts appear in the paper; the Chinese originals are preserved here as scientific research objects. See [`docs/TERMINOLOGY.md`](docs/TERMINOLOGY.md) for an EN–ZH glossary.

Code comments, historical notes, and source documents include Chinese; this README provides English and Chinese summaries.

## Citation

For these corrected materials, cite [release v1.2.0](https://github.com/stttttte/iso15189-llm-config-experiment/releases/tag/v1.2.0), archived at [DOI: 10.5281/zenodo.22855972](https://doi.org/10.5281/zenodo.22855972). [v1.1.0, DOI: 10.5281/zenodo.21769007](https://doi.org/10.5281/zenodo.21769007) identifies the historical archive, not this correction release.

1. Manuscript under revision for *Clinica Chimica Acta* (not yet published):
   ```
   Liu S, Yang L, Chen X, Wu D, Li D. (2026).
   Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents:
   Prompt Configuration, LLM-as-Judge Bias, and Exploratory Expert Validation.
   Manuscript in preparation/revision.
   ```

2. This repository:
   See [`CITATION.cff`](CITATION.cff) or use GitHub's "Cite this repository" button.

## License

- **Code** (`.py`, `.sh`): [MIT License](LICENSE)
- **Data and documents** (`.md`, `.json`, generated QMS files): [CC BY 4.0](LICENSE-DATA)

## Ethical Considerations

- **Research materials:** the generated QMS texts are drafting artifacts, not patient-level clinical observations. They require professional review before any operational use.
- **No API keys committed**: all LLM-API scripts read keys via environment variables.
- **Expert blind review:** configuration labels were concealed during scoring. The three raters are same-institution coauthors, so this is exploratory internal validation. The mapping is already recoverable from released results and is supplied as `data/expert_blind_review/blind_key.json` for reproduction; independent future review needs a newly blinded packet.
- **Rater informed consent**: Raters 2 and 3 provided informed consent prior to scoring. Their names and ID numbers are stripped from the released files; only role labels (e.g., "Rater 2, internal auditor") are retained.

## Acknowledgments

- Claude Opus 4.6 (Anthropic) — primary generation model + judge
- GPT-5.4 (OpenAI, via AIHubMix) — cross-model validation generation + judge
- Three same-institution laboratory experts — blinded document ratings
- `pingouin` (Vallat, 2018) — ICC computation

---

## 中文摘要

本仓库为一项针对 LLM 辅助 ISO 15189:2022 医学实验室质量管理体系（QMS）文件生成的研究提供数据和代码。

当前为作者确认的 v1.2.0 一致性修订版本（2026-09-20），已归档至 Zenodo，DOI：10.5281/zenodo.22855972。主分支的稿件和投稿信在归档完成后仅补入新 DOI，研究数据和分析不变；历史 v1.1.0 继续保留。

本次修订稿为 `paper/CCA_manuscript_consistency_revised.*`。原 CCLM 稿及 `Liu_2026_CCLM_*` 投稿文件保留为历史记录，其数值和结论不代表本次修订口径。

### 核心内容

- **486 篇 QMS 中文文件**：Claude 405 篇（9 组 × 15 任务 × 3 重复）；GPT 81 篇（9 组 × A1/B1/C1 三任务 × 3 重复）。
- **759 条归档文件级 LLM 评分**：GPT 486 条 + Claude 273 条。其他历史 Claude 均值只保留在 2×2 汇总中，无法完整恢复原始记录和分母。
- **30 份专家评分表**：10 篇 Claude 生成的 A 类文件 × 3 位同单位共同作者；专家间 ICC(2,k)=0.982。
- **离线复现材料**：三专家 ICC、九组综合排名、组分对照及配图；历史生成脚本需要路径适配、API 凭证及相关授权源模板。
- **配置文本大小清单**：按 cl100k_base 统计归档文本；不是已核实的 Claude 请求 token 数，也不构成最小有效 token 阈值。

### 核心发现

1. 探索性专家比较：专家均值与 Claude 的 ICC(3,1)=0.548，与 GPT 为 0.217；样本仅 10 篇。
2. 相对专家均值，Claude 平均高估 0.90 分，GPT 高估 0.52 分（0–5 分量表）。
3. H4 在自动评分与 GPT 评分合成的九组排名中居首；专家子样本中 F/H2/G 均值最高（4.06–4.24），H4 为 3.20，在有专家评分的七组中排第五。小样本且组间数量不等，不能确认最优配置。
4. 结构化组分对照并非田口正交设计：规则 Δ=+0.511（BH 校正 p=0.000562），骨架 Δ=+0.213（BH 校正 p=0.109，未达显著）。详细内容和示例的非显著结果不能证明无效。
5. 历史 2×2 汇总中 C_full 的表现随生成模型变化；不能据此推断 token 阈值或两模型实际输入等同。
6. 固定评审模型、比较生成模型的主分析差值为 Claude +0.294、GPT −0.301；固定生成模型、比较评审模型的敏感性差值为 +0.464、−0.472，两者含义不同。

### 使用与引用

- 详见英文部分
- 投稿正文为英文；本仓库的所有中文 QMS 生成文件是研究对象本身，故保留原文
- 代码采用 MIT 许可；数据采用 CC BY 4.0 许可
