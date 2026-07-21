# Supplementary Table S1

**Supplementary Table S1.** 本研究使用的 15 项 QMS 编写任务。每项任务在 9 组 prompt 配置下各重复 3 次（Claude Opus 4.6，共 405 份文件）；GPT-5.4 的跨模型验证只覆盖每类的第一项任务（A1、B1、C1）。任务的原始 user prompt 见 GitHub 仓库 `task_messages/`。

| 任务 ID | 任务名称 | 类别 | 期望篇幅 | 主要对应的 ISO 15189:2022 条款 |
|---|---|---|---|---|
| A1 | 新建人员管理程序文件 | A 文件编写 | 2500-3500字 | 6.2 人员 |
| A2 | 新建设备管理程序文件 | A 文件编写 | 3000-4000字 | 6.4 设备 |
| A3 | 新建检验前过程SOP | A 文件编写 | 2000-3000字 | 7.2 检验前过程 |
| A4 | 修订质量手册 | A 文件编写 | 800-1200字 | 8.2–8.4 文件与记录控制 |
| A5 | 修订记录表格 | A 文件编写 | 500-800字 | 6.4 设备（记录表格） |
| B1 | 生成年度内审检查表 | B 体系运行 | 表格形式，30-50条检查项 | 横跨第 4–8 章（全体系） |
| B2 | 生成特定模块内审检查表 | B 体系运行 | 表格形式，15-25条检查项 | 7.3 检验过程 |
| B3 | 迎检自查报告 | B 体系运行 | 1500-2500字 | 横跨第 4–8 章（45 个条款） |
| B4 | 管理评审输入材料 | B 体系运行 | 2000-3000字 | 8.9 管理评审 |
| B5 | 评审后整改计划 | B 体系运行 | 2000-3000字 | 8.6–8.7 纠正措施与不符合项 |
| C1 | 单文件审查——程序文件 | C 审核模拟 | 1500-2500字 | 横跨第 4–8 章（15 个条款） |
| C2 | 单文件审查——SOP | C 审核模拟 | 1200-2000字 | 横跨第 4–8 章（12 个条款） |
| C3 | 体系级审查 | C 审核模拟 | 1500-2500字 | 横跨第 4–8 章（52 个条款） |
| C4 | 审核驱动修改——文件更新 | C 审核模拟 | 1500-2500字 | 横跨第 4–8 章（12 个条款） |
| C5 | 审核驱动修改——整改闭环 | C 审核模拟 | 2000-3500字 | 7.5.5 / 8.7 不符合项与整改闭环 |

任务集覆盖的是文件控制、内审、迎检自查与管理评审一类的体系文件，其中包含纠正措施与整改闭环（B5、C5）以及横跨数十个条款的体系级审查（B3、C3）；不含检验方法确认与验证报告、测量不确定度评定程序、危急值报告与临床沟通记录、室间质评结果处理程序等技术类文件（见正文 §4.6 局限性 xviii）。

---

**Supplementary Table S1 (English).** The 15 QMS authoring tasks used in this study. Each task was run under all 9 prompt configurations with 3 replicates (Claude Opus 4.6; 405 documents in total); the GPT-5.4 cross-model validation covered only the first task of each class (A1, B1, C1). The original user prompts are available in the GitHub repository under `task_messages/`.

| Task ID | Task name | Class | Target length | Principal ISO 15189:2022 clause(s) |
|---|---|---|---|---|
| A1 | Draft a personnel-management procedure | A Document authoring | 2500-3500字 | 6.2 Personnel |
| A2 | Draft an equipment-management procedure | A Document authoring | 3000-4000字 | 6.4 Equipment |
| A3 | Draft a pre-examination SOP | A Document authoring | 2000-3000字 | 7.2 Pre-examination processes |
| A4 | Revise the quality manual | A Document authoring | 800-1200字 | 8.2–8.4 Document and record control |
| A5 | Revise a record form | A Document authoring | 500-800字 | 6.4 Equipment (record form) |
| B1 | Generate an annual internal-audit checklist | B System operation | 表格形式，30-50条检查项 | Spans Clauses 4–8 (whole system) |
| B2 | Generate a module-specific internal-audit checklist | B System operation | 表格形式，15-25条检查项 | 7.3 Examination processes |
| B3 | Pre-assessment self-inspection report | B System operation | 1500-2500字 | Spans Clauses 4–8 (45 clauses) |
| B4 | Management-review input material | B System operation | 2000-3000字 | 8.9 Management review |
| B5 | Post-review corrective action plan | B System operation | 2000-3000字 | 8.6–8.7 Corrective action and nonconformities |
| C1 | Single-document review — procedure document | C Audit simulation | 1500-2500字 | Spans Clauses 4–8 (15 clauses) |
| C2 | Single-document review — SOP | C Audit simulation | 1200-2000字 | Spans Clauses 4–8 (12 clauses) |
| C3 | System-level review | C Audit simulation | 1500-2500字 | Spans Clauses 4–8 (52 clauses) |
| C4 | Audit-driven revision — document update | C Audit simulation | 1500-2500字 | Spans Clauses 4–8 (12 clauses) |
| C5 | Audit-driven revision — CAPA closure | C Audit simulation | 2000-3500字 | 7.5.5 / 8.7 Nonconformity and CAPA closure |

The task set covers system-level documents concerned with document control, internal audit, pre-assessment self-inspection, and management review — including corrective action and CAPA closure (B5, C5) and system-wide reviews spanning dozens of clauses (B3, C3). It does not include technical documents such as method validation/verification reports, measurement-uncertainty procedures, critical-value reporting and clinical-communication records, or procedures for handling external quality assessment results (see §4.6, Limitation xviii).
