# Response to Reviewers — CCLM.2026.0735 (Resubmission)

> 随稿上传件（File Designation: Author's Response to Reviewer/Editor Critique，须排在上传文件第一位）。
> 引号内为修订稿原文，供审稿人直接核对。

---

## Response to Reviewers

**Manuscript CCLM.2026.0735 – resubmission**

**Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents: Prompt Configuration, LLM-as-Judge Bias, and Exploratory Expert Validation**

We are grateful to both reviewers. The two critiques pointed in different directions — one at what LLM drafting means for accreditation, the other at how the paper reads — and between them they have changed the manuscript a great deal.

A note on marking the changes. The revision touches nearly every section: the title is new, the main text is about 27% shorter, the Methods have been cut by more than 40%, all four figures have been redrawn, and the Limitations are now plain prose. Underlining what changed would leave almost the whole document underlined, so we have set out below what changed and where. We will gladly supply a marked copy if the editorial office prefers one.

Two changes of record. The title now names what the study actually did. And the author list has grown from one to five: Lan Yang and Xinying Chen served as Raters 2 and 3 on the blinded panel, Dan Wu handled data curation, and Dongdong Li supervised the work and is corresponding author. Individual roles are given in the Author Contributions statement, and all five authors have read and approved this version.

---

### Reviewer 1

The reviewer argues that ISO 15189 documentation is the tangible evidence that a laboratory operates in a controlled and competent way; that writing procedures is itself part of staff training, accountability, competence development and risk awareness; and that handing this work to AI would hollow out the accreditation process it is meant to support.

We agree, and we have rewritten the manuscript so that this is its position rather than a caveat inside it. We would add that our results make the same case from the data side: they show how far a well-formatted LLM draft can sit from actual compliance, and that only the human experts saw the difference.

Section 4.5 now states the constraint in the reviewer's own terms:

*"The drafting of QMS documents is not merely a clerical output; it is also the process through which laboratory staff build their sense of responsibility and risk awareness. If this work is delegated entirely to an LLM, staff gradually lose writing practice and struggle to develop a deep understanding of the ISO 15189 process as a whole. We therefore regard human supervision as a constraint on the use of LLMs in this setting. ISO 15189:2022 requires competent personnel and a complete examination process, not merely well-formatted documents."*

This is consistent with the published consensus that LLMs in healthcare quality management belong in clerical tasks performed under mandatory human verification (reference [14]). The Conclusions now end on the same point:

*"Ultimately, ISO 15189 documentation is the process by which laboratory staff learn processes and risks, take responsibility, and demonstrate competence; an LLM can take over only its routine textual work – expert final review remains indispensable."*

Throughout the revised text, no configuration is described as producing anything more than a reference draft. What decides whether a document can actually be used for accreditation — the laboratory's own quality-control data, its patient data distributions, its proficiency-testing history — has to be entered and interpreted by competent staff, because the model holds none of it. Section 4.4 is now titled "Provisional configuration guidance", and every scenario in Table 4 ends with revision by laboratory staff and expert sign-off.

Our numbers support the concern. Both LLM judges rated compliance 0.52–0.90 points above the expert panel. The configuration the judges ranked first fell to fifth under expert review, only 0.16 points above a document produced with no prompt at all. And the documents the judges overrated most were precisely the ones that look right — correct structure, correct terminology — but carry no clinically grounded operational detail (Section 3.5). We are not proposing that LLMs replace laboratory staff. The study set out to find where the safe boundary lies, and the data put that boundary considerably further back than LLM-based evaluation alone would suggest.

---

### Reviewer 2

**2.1 The paper is too dense to read; interpretive sentences are scattered among technical details; shorten it and emphasize the key points.**

This was fair, and it drove the largest part of the revision. The main text is about 27% shorter than the version reviewed (roughly 7,500 to 5,500 words), with the Methods cut by more than 40%. Implementation detail moved to the Supplementary Material rather than being deleted, and every methodological statement is still made in the main text.

The Conclusions were the clearest case: 444 words rewritten into about 220, as a single argument running from the finding to its practical consequences to the closing position, with topic sentences carrying the thread (*"Nor is more context safer"*; *"Evaluation, too, cannot be delegated"*). The Limitations, previously an enumerated list, are now six paragraphs of prose. Redundant cross-references were pruned, and the remaining statistics all follow one bracket format. A small table on self-preference bias became a single sentence, and the per-dimension and per-task-class effects were consolidated into Table 2 instead of appearing scattered through the prose. The scoring rubric, previously a main-text table, moved to Supplementary Table S2; the four remaining tables carry the results, which also keeps the display items within the journal limit.

**2.2 In the abstract it is not clear what C_full is; the explanation comes later.**

The abstract now names it at first mention — *"the full-context C_full (~56,000 tokens)"* — with the full definition still in Section 2.1.

**2.3 The references at the start of the Introduction are misnumbered: the first is 7, the second 14.**

Our mistake. The reference list has been renumbered from scratch. The Introduction now opens with [1] and [2], and the list contains 14 references numbered in order of first citation.

**2.4 Figure 1 needs clarifying: C_full is longer yet seems to contain less material.**

The reviewer identified a genuine ambiguity in the original design, and the figure has been rebuilt around it. Component presence (included / partial / absent) and total prompt size are now shown as two separate encodings, and the caption says plainly that they are not proportional: the component marks index distilled, structured prompt content, whereas bar length reflects the total volume of loaded text. C_full reaches the largest token count by loading the full raw reference corpus, yet its rules mark is only partial, because in that configuration the rules sit buried in raw text rather than being supplied as a distilled rule set.

**2.5 Figure 3: seven colors in the legend, nine dots in the left panel, ten in the right; some colors duplicated, some missing.**

The scatter plot has been replaced by a Bland–Altman analysis. Each panel now shows exactly the ten expert-reviewed documents, colored by four configuration families, with an open circle for the no-prompt baseline; the legend matches the marks used, and nothing is duplicated or missing. All four figures were redrawn with one colorblind-safe palette applied consistently.

**2.6 Avoid deep technical detail unless it serves the reader; gather numbers into tables rather than scattering them in parentheses.**

Done as part of the condensation above. Stratified and per-dimension effect estimates now sit in Table 2; document counts, model parameters and rating tallies are stated once in the Methods rather than repeated; and parenthetical numbers in the Discussion were removed except where a claim depends on them.

---

### Other changes made during the revision

We also checked the manuscript against our released code and corrected the methodological reporting. The generation and judging parameters of both models are now stated exactly (Sections 2.2 and 2.3.2). The Claude judge's coverage — 378 document-level ratings, 77.8% — is explained: the judging ran in batches as the configuration set grew, and for some batches only group-level means were kept. Section 2.4.1 acknowledges that replicates sharing the same tasks are not fully independent, and Section 2.3.1 states where the automated scorer's weights come from.

An "Acknowledgment of AI tool use" section has been added to the manuscript, following the De Gruyter Brill AI Policy for Authors: AI as research object, AI as evaluator, AI-assisted drafting, figure integrity, and accountability. The public repository and archive have been updated to match this version (GitHub; Zenodo v1.1.0), and the manuscript now cites the version-independent concept DOI 10.5281/zenodo.20091463.

Both reviewers have left the manuscript clearer and more honest about its limits, and we thank them for the time they gave it.
