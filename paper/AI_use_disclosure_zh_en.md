# Acknowledgement of AI Tool Use — 中英双版

> 为 CCLM（De Gruyter Brill）投稿准备。符合其 AI Policy for Authors 条款。
> 中文版可放入中文版本的论文致谢章节；英文版用于最终英文投稿的 Acknowledgements 节。

---

## 英文版（投稿使用）

### Acknowledgement of AI tool use

In accordance with the AI Policy for Authors of De Gruyter Brill, the author discloses the following use of generative artificial-intelligence (AI) tools in this work.

**1. AI as research objects.** Claude Opus 4.6 (Anthropic, San Francisco, USA) and GPT-5.4 (OpenAI, San Francisco, USA, accessed via the AIHubMix API proxy) were used to generate the 486 ISO 15189:2022 quality-management-system (QMS) documents that constitute the primary dataset of this study. These documents are the experimental object under investigation; they are neither fabricated clinical data nor intended to be used in real patient care.

**2. AI as evaluators.** Claude Opus 4.6 and GPT-5.4 were additionally used as LLM judges to produce 864 document evaluations under a CNAS-style reviewer prompt, as described in Section 2.3. Full prompts, model parameters, and per-paper scores are provided in the public repository (https://github.com/stttttte/iso15189-llm-config-experiment).

**3. AI-assisted manuscript drafting.** The author used Claude Code (Claude Opus 4.6, Anthropic) to assist with manuscript outlining, first-draft composition, table preparation, and data-visualisation code generation. All AI-suggested content, wording, and analytical code were critically reviewed, revised, and verified by the human author. The author takes sole responsibility for the final manuscript, including all claims, interpretations, and conclusions.

**4. No AI-generated images or manipulated data.** All figures (Figures 1–4) were produced using matplotlib 3.7.1 (Python 3.11) from raw numerical data stored as JSON files. No generative AI tools were used to create, alter, or manipulate images, figures, or numerical data. Inter-rater reliability statistics [ICC(2,1) and ICC(3,1)] were calculated using pingouin 0.5. Raw data and analysis scripts are openly available in the repository above.

**5. Chain of accountability.** The author confirms compliance with De Gruyter Brill's AI Policy for Authors and accepts full responsibility for all content of this submission, in accordance with the ICMJE authorship criteria.

---

## 中文版（中文稿致谢段落使用）

### AI 工具使用披露

依据 De Gruyter Brill 出版社《AI Policy for Authors》的要求，作者就本研究使用生成式人工智能（AI）工具的情况披露如下。

**1. AI 作为研究对象**。本研究使用 Claude Opus 4.6（Anthropic 公司）与 GPT-5.4（OpenAI 公司，经 AIHubMix 代理接入）生成共 486 份 ISO 15189:2022 质量管理体系（QMS）文件，作为研究的主要数据集。这些文件是研究考察的实验对象，既非伪造的临床数据，亦未用于真实临床实践。

**2. AI 作为评审员**。Claude Opus 4.6 与 GPT-5.4 在本研究中另作为 LLM 评审员，按照 CNAS 评审员视角的 prompt 对文件打分，共完成 864 次评分。完整 prompt、模型参数与逐篇评分数据已公开于研究仓库（https://github.com/stttttte/iso15189-llm-config-experiment）。

**3. AI 辅助稿件起草**。作者使用 Claude Code（基于 Claude Opus 4.6）协助稿件的大纲撰写、初稿起草、表格整理与数据可视化代码生成。所有 AI 建议的内容、措辞与分析代码均经作者批判性审阅、修改与验证。作者对本稿件最终文本中的所有陈述、解释与结论承担全部责任。

**4. 无 AI 生成图像或被操纵数据**。全部 4 张图（Figure 1–4）采用 matplotlib 3.7.1（Python 3.11）从 JSON 格式的原始数值数据绘制。本研究未使用任何生成式 AI 工具创建、修改或操纵图像或数值数据。评分者间一致性统计量 [ICC(2,1) 与 ICC(3,1)] 由 pingouin 0.5 计算。原始数据与分析脚本已在上述仓库公开。

**5. 责任声明**。作者确认本研究符合 De Gruyter Brill 出版社《AI Policy for Authors》的各项条款，并依照 ICMJE 作者身份标准对本稿件全部内容承担全部责任。

---

## 使用方式

- 中文稿致谢节：把上面"中文版"整段粘入《论文正文v2_中文_CCLM.md》的"申报声明"之后、"致谢"之前
- 最终英文投稿：把"英文版"整段粘入 Acknowledgements 或 Competing interests 附近，CCLM 投稿系统一般有 "Declarations" 专区
- Cover letter 里**简短呼应**（见 cover_letter_CCLM.md）
