# Acknowledgment of AI Tool Use — 中英双版

> 为 CCLM（De Gruyter Brill）投稿准备，符合其 AI Policy for Authors 条款。
> 本内容已并入正文（英文稿 Acknowledgments 节、中文稿致谢节）；此文件供投稿系统需要单独上传 AI disclosure 附件时使用。
> 口径与正文一致：五作者、864 = GPT 486 + Claude 378（文件级）、批次+组均值原因见正文第 2.3.2 节与第 4.6 节。

---

## 英文版（投稿使用）

### Acknowledgment of AI tool use

In accordance with the AI Policy for Authors of De Gruyter Brill, the authors disclose the following use of generative artificial intelligence (AI) tools in this work.

**1. AI as research objects.** Claude Opus 4.6 (Anthropic, San Francisco, CA, USA) and GPT-5.4 (OpenAI, San Francisco, CA, USA, accessed via the AIHubMix API proxy) were used to generate the 486 ISO 15189:2022 quality-management-system (QMS) documents that constitute the primary dataset of this study. These documents are the experimental objects under investigation; they are not fabricated clinical data and were not used in real patient care.

**2. AI as evaluators.** The same two models served as LLM judges, producing the 864 retained document-level ratings described in Section 2.3 of the manuscript (486 GPT-judge ratings covering all documents and 378 Claude-judge ratings covering 77.8%). The Claude judging ran in successive batches as the configuration set expanded, and for some batches only group-level means were retained (Sections 2.3.2 and 4.6). Full prompts, model parameters, and per-document score files are provided in the public repository (https://github.com/stttttte/iso15189-llm-config-experiment).

**3. AI-assisted manuscript drafting.** The first author used Claude Code (Claude Opus 4.6, Anthropic) to assist with manuscript outlining, first-draft composition, table preparation, and data-visualization code generation. All AI-suggested content, wording, and analytical code were critically reviewed, revised, and verified by the authors, who take full responsibility for the final manuscript, including all claims, interpretations, and conclusions.

**4. No AI-generated images or manipulated data.** All figures (Figures 1–4) were produced with matplotlib 3.7.1 (Python 3.11) from raw numerical data stored as JSON files. No generative AI tools were used to create, alter, or manipulate images, figures, or numerical data. Inter-rater reliability statistics were calculated with pingouin 0.5.

**5. Accountability.** The authors confirm compliance with De Gruyter Brill's AI Policy for Authors and accept full responsibility for all content of this submission, in accordance with the ICMJE authorship criteria.

---

## 中文版（中文稿致谢段落使用）

### AI 工具使用披露

依据 De Gruyter Brill 出版社《AI Policy for Authors》的要求，作者就本研究使用生成式人工智能（AI）工具的情况披露如下。

**1. AI 作为研究对象**。本研究使用 Claude Opus 4.6（Anthropic 公司）与 GPT-5.4（OpenAI 公司，经 AIHubMix 代理接入）生成共 486 份 ISO 15189:2022 质量管理体系（QMS）文件，作为研究的主要数据集。这些文件是研究考察的实验对象，不是伪造的临床数据，也未用于真实临床实践。

**2. AI 作为评审员**。同样两个模型在本研究中担任 LLM 评判者，产生正文第 2.3 节所述的 864 条文件级评分（GPT 评判者 486 条覆盖全部文件，Claude 评判者 378 条覆盖 77.8%）。Claude 评审随配置集扩展分批进行，部分批次仅保留组均值而非逐文件评分（详见正文第 2.3.2 节与第 4.6 节）。完整 prompt、模型参数与逐文件评分数据已公开于研究仓库（https://github.com/stttttte/iso15189-llm-config-experiment）。

**3. AI 辅助稿件起草**。第一作者使用 Claude Code（基于 Claude Opus 4.6）协助稿件的大纲撰写、初稿起草、表格整理与数据可视化代码生成。所有 AI 建议的内容、措辞与分析代码均经作者批判性审阅、修改与验证，作者对最终稿件中的所有陈述、解释与结论承担全部责任。

**4. 无 AI 生成图像或被操纵数据**。全部 4 张图（Figure 1–4）采用 matplotlib 3.7.1（Python 3.11）从 JSON 格式的原始数值数据绘制。本研究未使用任何生成式 AI 工具创建、修改或操纵图像或数值数据。评分者间一致性统计量由 pingouin 0.5 计算。

**5. 责任声明**。作者确认本研究符合 De Gruyter Brill 出版社《AI Policy for Authors》的各项条款，并依照 ICMJE 作者身份标准对本稿件全部内容承担全部责任。
