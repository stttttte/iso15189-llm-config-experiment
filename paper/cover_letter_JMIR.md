5 August 2026

Dear Professor Benis and the Editorial Team,

We are pleased to submit our original research manuscript, "Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents: Input Specification, LLM-as-Judge Bias, and Exploratory Expert Validation," for consideration by *JMIR Medical Informatics*. We believe it fits the journal's AI Language Models in Health Care section.

Medical laboratories seeking ISO 15189 accreditation must produce on the order of 100-300 controlled quality management system (QMS) documents, a task that typically occupies an in-house quality team for months. Large language models (LLMs) could ease this burden, but putting them to use raises two open questions: what input must the model be given, and can another LLM be trusted to score the output? There is little empirical evidence on either; this study explores both.

Across 486 generated documents, 864 LLM-judge ratings, and blinded review by three qualified internal auditors, three findings stand out:

1. **Input specification, not prompt bulk, determines output quality.** Of four prompt components, only distilled requirement rules significantly improved compliance (Δ=0.511); a ~56,000-token full-context prompt collapsed under one generation model, so loading more material is no substitute for stating requirements.

2. **The "best" configuration depends on who evaluates it.** The configuration LLM judges ranked first fell to fifth under blinded expert review, whereas template-anchored prompts earned the highest expert scores.

3. **LLM-as-judge overestimates expert-rated compliance by 0.52-0.90 points**, with preference patterns incompatible with classical self-preference; it can support first-pass screening before expert review but cannot replace it.

The study puts LLM scoring and blinded expert scoring side by side on the same documents and measures how far apart they are. For readers using or evaluating language models in health care, it offers a concrete reference point: where LLM scores and expert judgment part ways, by how much, and which configurations are worth choosing when human verification is mandatory. The natural next step is to have laboratory professionals formulate their local process requirements before generation begins; this approach is currently under evaluation.

All generated documents, ratings, and analysis code are openly available on GitHub (https://github.com/stttttte/iso15189-llm-config-experiment) and archived on Zenodo (DOI: 10.5281/zenodo.20091463). The study involved no patient data; written informed consent was obtained from the two raters who are co-authors. The authors declare no competing interests and no relationships with any LLM provider. The manuscript is not under consideration elsewhere, and all authors have approved the submission. We agree to pay the article processing fee upon acceptance.

**Suggested reviewers.** We respectfully suggest the following specialists in the evaluation of language models in health care:

1. **Dr. Danielle L. Mowery** - Chief Research Information Officer, Perelman School of Medicine, University of Pennsylvania, Philadelphia, PA, USA. Email: danielle.mowery@pennmedicine.upenn.edu. Expertise: clinical natural language processing and evaluation methodology; co-author of a 2026 scoping review of LLM-as-a-judge in healthcare.

2. **Prof. Harold P. Lehmann** - Professor of Health Sciences Informatics, Johns Hopkins University School of Medicine, Baltimore, MD, USA. Email: lehmann@jhmi.edu. Expertise: evaluation methodology for clinical informatics and decision support; co-author of a 2026 scoping review of LLM-as-a-judge in healthcare.

3. **Dr. Veysel Kocaman** - Chief Technology Officer, John Snow Labs, Lewes, DE, USA. Email: veysel@johnsnowlabs.com. Expertise: first author of the CLEVER framework (JMIR AI, 2025) comparing expert review with LLM performance on clinical text tasks.

4. **Dr. Andrew Y. Shin** - Department of Pediatrics, Stanford University School of Medicine, Stanford, CA, USA. Expertise: senior author of a dual-perspective (physician and family) evaluation of LLM-generated clinical summaries (JMIR AI, 2026).

Thank you for your consideration. We look forward to your response.

Sincerely,

**Dongdong Li**, on behalf of all authors

Department of Laboratory Medicine, West China Hospital, Sichuan University

Sichuan Clinical Research Center for Laboratory Medicine

Chengdu, Sichuan, PR China

Email: jiangxili1219@163.com

ORCID: 0000-0002-0290-6485

---

<!--internal-->

## 自用注释（不随稿提交）

- 收信人 Arriel Benis：2025 年起任 JMIR Medical Informatics 主编（官方公告已核实），投稿当天再看一眼有无变动
- 全信不提 CCLM 投稿史；JMIR 系统若问"是否曾投他刊/被拒"，如实勾选即可
- Shin 无公开邮箱（已查，斯坦福临床医生不公开），信里不写；系统表单若强制邮箱则只填前三位，或整体跳过（JMIR 建议审稿人为可选项）
- 四位审稿人：两位方法学（Mowery/Lehmann，同一综述不同单位）+ 一位工业评估框架（Kocaman）+ 一位临床评估实践（Shin）；无中国专家、无 ISO 15189 圈内人
- JMIR 投稿在 mc04.manuscriptcentral.com/jmir 系（或其新系统），cover letter 通常粘贴为文本
