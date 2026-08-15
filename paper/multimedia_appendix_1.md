# Multimedia Appendix 1

All documents in this study were generated and evaluated in Chinese. The tables below are English translations; the original Chinese wording of the task prompts and the scoring rubric, as actually deployed, is available in the public repository (https://github.com/stttttte/iso15189-llm-config-experiment).

**Table S1.** The 15 QMS authoring tasks used in this study. Each task was run under all 9 prompt configurations with 3 replicates (Claude Opus 4.6; 405 documents in total); the GPT-5.4 cross-model validation covered only the first task of each class (A1, B1, C1). The original user prompts are available in the GitHub repository under `task_messages/`.

| Task ID | Task name | Class | Target length | Principal ISO 15189:2022 clause(s) |
|---|---|---|---|---|
| A1 | Draft a personnel-management procedure | A Document authoring | 2500-3500 characters | 6.2 Personnel |
| A2 | Draft an equipment-management procedure | A Document authoring | 3000-4000 characters | 6.4 Equipment |
| A3 | Draft a pre-examination SOP | A Document authoring | 2000-3000 characters | 7.2 Pre-examination processes |
| A4 | Revise the quality manual | A Document authoring | 800-1200 characters | 8.2–8.4 Document and record control |
| A5 | Revise a record form | A Document authoring | 500-800 characters | 6.4 Equipment (record form) |
| B1 | Generate an annual internal-audit checklist | B System operation | checklist format, 30-50 check items | Spans Clauses 4–8 (whole system) |
| B2 | Generate a module-specific internal-audit checklist | B System operation | checklist format, 15-25 check items | 7.3 Examination processes |
| B3 | Pre-assessment self-inspection report | B System operation | 1500-2500 characters | Spans Clauses 4–8 (45 clauses) |
| B4 | Management-review input material | B System operation | 2000-3000 characters | 8.9 Management review |
| B5 | Post-review corrective action plan | B System operation | 2000-3000 characters | 8.6–8.7 Corrective action and nonconformities |
| C1 | Single-document review — procedure document | C Audit simulation | 1500-2500 characters | Spans Clauses 4–8 (15 clauses) |
| C2 | Single-document review — SOP | C Audit simulation | 1200-2000 characters | Spans Clauses 4–8 (12 clauses) |
| C3 | System-level review | C Audit simulation | 1500-2500 characters | Spans Clauses 4–8 (52 clauses) |
| C4 | Audit-driven revision — document update | C Audit simulation | 1500-2500 characters | Spans Clauses 4–8 (12 clauses) |
| C5 | Audit-driven revision — CAPA closure | C Audit simulation | 2000-3500 characters | 7.5.5 / 8.7 Nonconformity and CAPA closure |

The task set covers system-level documents concerned with document control, internal audit, pre-assessment self-inspection, and management review — including corrective action and CAPA closure (B5, C5) and system-wide reviews spanning dozens of clauses (B3, C3). It does not include technical documents such as method validation/verification reports, measurement-uncertainty procedures, critical-value reporting and clinical-communication records, or procedures for handling external quality assessment results (see Section 4.6, Limitation xviii).

---

**Table S2. Five-dimensional descriptive rubric shared by Tiers 2a, 2b, and 3.**

| Dimension | Anchor at 5 | Anchor at 3 | Anchor at 1 |
|-----------|-------------|-------------|-------------|
| Clause coverage | All "shall" requirements of the relevant clauses are operationalized through concrete measures | Major clauses are covered but with omissions or surface-level treatment | Most clauses are merely cited without implementation, or major omissions are evident |
| Operability | Every step has a named role (job title), a quantified deadline, and an explicit output (form ID) | Most steps are actionable; a few remain vague | Pervasive use of "in a timely manner", "relevant personnel", and "periodically" without operational detail |
| Internal consistency | All referenced documents and forms appear in the corresponding sections; responsibilities are cleanly assigned | A few dangling references or minor textual contradictions | Many dangling references or conflicting responsibility assignments |
| PDCA closure | An explicit Plan–Do–Check–Act chain with execution records, effectiveness evaluation, non-conformity handling, and improvement | P–D–C are present but A (improvement/feedback) is missing | Execution steps only; no checking or improvement |
| Professional depth | Contains laboratory-specific detail (e.g., Westgard rules, measurement uncertainty, Sigma metrics, HIL indices, blind testing, PCR zoning, cold chain) | Some professional flavor, but largely generic | Generic content equally applicable to any laboratory |

<!--tbl-note-->This rubric was shared by Tier 2 (LLM judges) and Tier 3 (expert review). Anchor descriptions for scores of 5, 3, and 1 are given above; the intermediate scores 4 and 2 fall between adjacent anchors, and 0 means the dimension could not be evaluated. The anchor descriptions were identical for all judges and experts.
