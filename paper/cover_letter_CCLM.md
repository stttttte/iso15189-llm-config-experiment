# Cover Letter for CCLM Resubmission

> Target journal: *Clinical Chemistry and Laboratory Medicine* (CCLM), De Gruyter Brill
> Manuscript type: Original Article（reject-and-resubmit 重投版）
> Submission system: Editorial Manager

---

## 英文版（投稿使用）

[Date]

Dear Editor-in-Chief,

We are pleased to submit our original research manuscript entitled **"Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents: Prompt Configuration, LLM-as-Judge Bias, and Exploratory Expert Validation"** for consideration for publication in *Clinical Chemistry and Laboratory Medicine*.

This manuscript is a revised version of our earlier submission to CCLM (Manuscript No. CCLM.2026.0735), which received a reject-and-resubmit decision. The present version has been extensively revised in response to the reviewers' comments – including corrected methodological reporting, a restructured Limitations section, redesigned figures, and substantially condensed text – and is accompanied by a point-by-point response.

Medical laboratories seeking ISO 15189 accreditation must produce on the order of 100–300 controlled quality management system (QMS) documents, a process that typically takes an in-house quality team several months. Large language models (LLMs) are increasingly used to accelerate this drafting, yet laboratories currently have no empirical evidence on how to prompt these models, nor on whether LLM-based scoring can be trusted to evaluate the output. Our study addresses both questions directly.

We generated 486 QMS documents across nine prompt configurations using two state-of-the-art LLMs, and evaluated them through a three-tier framework: an automated rule-based scorer, two LLM judges (864 ratings), and blinded review by three qualified ISO 15189 internal auditors. Three findings should be of practical interest to your readership:

1. **The "best" prompt configuration depends on who evaluates it.** Minimal prompts (~1,000–2,000 tokens) ranked first under LLM-based scoring but fell to fifth under expert review, whereas template-anchored prompts (~15,000–16,000 tokens) achieved the highest expert scores. Token efficiency and accreditation readiness are distinct optimization targets.

2. **LLM-as-judge systematically overestimates expert-rated compliance** by 0.52–0.90 points and shows model-dependent preference patterns incompatible with classical self-preference. LLM judges may serve as first-pass screening filters, but cannot substitute for expert review of documents intended for accreditation.

3. **More context is not safer.** A ~56,000-token full-context prompt collapsed under one generation model, with declining instruction-following and confused or fabricated clause citations – cautioning against the intuitive "load everything" strategy.

To our knowledge, this is the first systematic comparison of prompt configurations for ISO 15189 document drafting with quantification of LLM-judge bias against expert validation. The provisional, scenario-stratified configuration guidance we provide is immediately usable by laboratories adopting LLM-assisted drafting under mandatory human verification.

All generated documents, LLM-judge ratings, expert ratings, and analysis code are openly available on GitHub (https://github.com/stttttte/iso15189-llm-config-experiment) and archived on Zenodo (DOI: 10.5281/zenodo.20091463). The study involved no patient data; written informed consent was obtained from the two participating raters who are co-authors. The authors declare no competing interests and no relationships with any LLM provider. The manuscript is original, has not been published previously, and is not under consideration by any other journal. All authors have read and approved the submission.

**Suggested reviewers.** We respectfully suggest the following specialists with relevant expertise in laboratory QMS, ISO 15189, and/or LLM evaluation:

1. **Dr. Hikmet Can Çubukçu, MD, Assoc. Prof.** – Rare Diseases Department, General Directorate of Health Services, Turkish Ministry of Health, Ankara, Türkiye. Email: hikmetcancubukcu@gmail.com. ORCID: 0000-0001-5321-9354. *Expertise: ISO 15189:2022 (co-author of the EFLM Working Group on Accreditation revision-analysis paper, CCLM 2025) and AI in laboratory medicine.*

2. **Dr. Tze Ping Loh** – Department of Laboratory Medicine, National University Hospital, Singapore. Email: Tze_ping_loh@nuhs.edu.sg. *Expertise: machine learning and AI applications in clinical chemistry; patient-based real-time quality control; frequent CCLM author.*

3. **Prof. Marc H. M. Thelen** – Foundation for Quality Assessment in Medical Laboratories (SKML) and Department of Laboratory Medicine, Radboud University Medical Center, Nijmegen, The Netherlands. Email: mthelen@skml.nl. *Expertise: ISO 15189 accreditation and metrological traceability; core member of the EFLM Working Group on Accreditation and ISO/CEN Standards.*

Thank you for your consideration. We look forward to your response.

Sincerely,

**Dongdong Li**, on behalf of all authors

Department of Laboratory Medicine, West China Hospital, Sichuan University

Sichuan Clinical Research Center for Laboratory Medicine

Chengdu, Sichuan, PR China

Email: jiangxili1219@163.com

ORCID: 0000-0002-0290-6485

---

## 中文辅助注释（不随稿提交，仅自用）

- **[Date]** 填投稿当日；如系统允许指名主编，把 "Dear Editor-in-Chief" 换成现任主编姓名（投稿前在 CCLM 官网核实）
- 重投段落（第 2 段，引用 CCLM.2026.0735）是本轮新增——若你决定按全新投稿处理、不提前稿，删掉该段即可
- 三位建议审稿人沿用首投版名单；若系统提示"曾评审过本稿"冲突，可换人
- 信中 "To our knowledge, this is the first..." 保留是恰当的——cover letter 是向编辑推销新颖性的场合，与正文语气不同
- 随稿附件清单：manuscript（含图版 docx/PDF）+ figures ×4（PNG 300dpi）+ Supplementary Table S1 + AI disclosure + point-by-point response + 本信
