# Terminology Glossary (ZH–EN)

For international readers of the English paper reviewing the Chinese-language generated QMS documents.

---

## 1. Standards and accreditation bodies

| 中文 | English | Notes |
|------|---------|-------|
| ISO 15189:2022 | ISO 15189:2022 | Medical laboratory QMS standard |
| CNAS | CNAS | China National Accreditation Service for Conformity Assessment |
| CNAS-CL02:2023 | CNAS-CL02:2023 | Chinese adoption of ISO 15189 (the version in force during our experiment) |
| 主任评审员 | Senior (lead) assessor | CNAS role title |
| SHALL 要求 | SHALL requirement | Mandatory normative requirement |

## 2. Document types

| 中文 | English |
|------|---------|
| 质量管理体系 (QMS) | Quality Management System |
| 质量手册 | Quality manual |
| 程序文件 / 控制程序 | Controlled procedure / control program |
| 作业指导书 (SOP) | Standard Operating Procedure |
| 记录表单 / 记录表格 | Record form |
| 修订历史 / 变更历史 | Revision history |
| 文件受控状态 | Document controlled status |
| 审查报告 | Audit / review report |
| 内审检查表 | Internal audit checklist |
| 管理评审输入材料 | Management review input materials |
| 纠正措施报告 | Corrective action report |

## 3. Quality management concepts

| 中文 | English | Anchors / notes |
|------|---------|-----------------|
| 检验前/中/后过程 | Pre-/intra-/post-examination process | NOT "analytical phase" (legacy wording) |
| 不确定度 / 测量不确定度 | Measurement uncertainty | |
| 生物参考区间 | Biological reference interval | NOT "normal range" |
| 样品 | Sample | (NOT 标本) |
| 检测项目 | Examination item | (NOT 检验项目) |
| 正确度 | Trueness | (NOT 准确度) |
| 精密度 | Precision | |
| 质控物 | Quality control material | (NOT 质控品) |
| 可报告范围 | Reportable range | (NOT 线性范围) |
| 能力评估 / 能力验证 | Competence assessment / Proficiency testing | NOT 室间质评 for PT |
| 授权 | Authorization | |
| PDCA 闭环 | PDCA cycle (Plan-Do-Check-Act) | |

## 4. Clinical / technical terms

| 中文 | English | Context |
|------|---------|---------|
| Westgard 规则 | Westgard multi-rule | QC rules |
| Sigma 度量 | Sigma metrics | Quality metric |
| HIL 指数 | HIL index (Hemolysis/Icterus/Lipemia) | Sample quality |
| 盲样测试 | Blind sample testing | |
| PCR 分区 | PCR zoning | Molecular lab setup |
| 冷链 | Cold chain | Sample transport |
| 产前筛查 | Prenatal screening | |
| 新生儿筛查 | Newborn screening | |
| 妇幼保健院 | Maternal and Child Health Hospital | Generic institution type |
| POCT | Point-of-Care Testing | |
| cfDNA | Cell-free DNA | Molecular diagnostics |
| 血培养 | Blood culture | Microbiology |

## 5. Task categories in the experiment

| 中文 | English |
|------|---------|
| A 类（文件编写） | Class A — Document authoring |
| B 类（体系运行） | Class B — System operation |
| C 类（审核模拟） | Class C — Audit simulation |

### Task ID reference (A1–C5)

| Task | Chinese | English short name |
|------|---------|--------------------|
| A1 | 人员培训与能力评估控制程序 | Personnel training & competence assessment SOP |
| A2 | 设备管理控制程序 | Equipment management SOP |
| A3 | 样本采集与处理 SOP | Sample collection & handling SOP |
| A4 | 管理评审修订（质量手册章节） | Management review revision (quality manual chapter) |
| A5 | 设备校准记录表（修订） | Equipment calibration record form (revised) |
| B1 | 年度内审检查表 | Annual internal audit checklist |
| B2 | 检验过程质量控制专项内审检查表 | Examination-process QC internal audit checklist |
| B3 | 迎检自查报告 | Pre-inspection self-audit report |
| B4 | 管理评审输入材料 | Management review input materials |
| B5 | 评审后整改计划及验证方案 | Post-audit corrective action plan |
| C1 | 内部质控程序文件审查报告 | Internal QC procedure review report |
| C2 | 生化分析仪 SOP 审查报告 | Biochemistry analyzer SOP review report |
| C3 | 体系级覆盖完整性审查报告 | System-level coverage completeness audit |
| C4 | 审核驱动修改——文件更新 | Audit-driven document update |
| C5 | 整改闭环——纠正措施报告 | Corrective action closure report |

## 6. Vagueness bans (规则层中的 7 类禁令)

These are expressions flagged by the auto-scorer's "vagueness" detector:

| 中文禁用表述 | English literal | Why banned | Required replacement |
|--------------|----------------|------------|---------------------|
| 大约 / 约 | "approximately" | Non-quantitative | Specific numeric value |
| 一般来说 / 通常 | "generally / usually" | Ambiguous scope | Delete, or state "except for X" |
| 及时 / 尽快 | "timely / ASAP" | No actionable deadline | Concrete time limit |
| 相关人员 | "relevant personnel" | Non-specific role | Specific job title |
| 适当 / 合理 / 必要时 | "appropriate / reasonable / when necessary" | No trigger condition | Explicit trigger |
| 定期 / 经常 | "periodic / frequent" | No frequency | Concrete frequency |
| 做好记录 | "record well" | No form reference | Reference specific form number |

## 7. Configuration group names (for reviewers)

See [DATA_DICTIONARY.md §7](DATA_DICTIONARY.md#7-group-naming-conventions) for the full definition.

| Group | Token count | Composition (plain English) |
|-------|-------------|-----------------------------|
| A_bare | 0 | No configuration (bare user prompt only) |
| B_simple | 0.4K | Minimal system prompt |
| C_full | 71K | Full dump (all rules, skeleton, detail, examples) |
| E_rules_v2 | 3.1K | Rules layer only |
| F_template | 35K | Template layer only (skeleton + detail, no rules) |
| G_template_rules | 38K | Rules + template (no examples) |
| H2_keep_examples | 61K | Rules + template + examples |
| H3_skeleton | 13K | Rules + module-level skeleton only |
| **H4_sop_only** | **6K** | **Rules + task-specific SOP skeleton only** (LLM-layer optimum) |

## 8. Abbreviations

| Abbreviation | Meaning |
|--------------|---------|
| QMS | Quality Management System |
| SOP | Standard Operating Procedure |
| CNAS | China National Accreditation Service |
| ICC | Intraclass Correlation Coefficient |
| PT | Proficiency Testing |
| IQC | Internal Quality Control |
| EQA | External Quality Assessment |
| HIL | Hemolysis / Icterus / Lipemia |
| PCR | Polymerase Chain Reaction |
| POCT | Point-of-Care Testing |
| LLM | Large Language Model |
