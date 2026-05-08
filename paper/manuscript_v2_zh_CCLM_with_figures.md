# LLM 生成医学实验室 QMS 文件的 ISO 15189 合规性：Claude Opus 4.6 vs. GPT-5.4 跨 prompt 配置评估

**作者**：刘斯迪（Sidi Liu）¹

**单位**：¹ 四川大学华西厦门医院检验科，福建厦门 361024，中国

**通讯作者**：刘斯迪，lllsssddd@icloud.com，ORCID: 0009-0006-1695-5372

**Short title**：Prompting strategies for ISO 15189 document compliance

**关键词**：ISO 15189；医学实验室；质量管理体系；大语言模型；prompt engineering；LLM-as-judge；专家验证

---

## 摘要

**Objectives**：比较 LLM 生成 QMS 文件在不同 prompt 配置下的 ISO 15189:2022 合规性，并刻画 LLM-as-judge 偏差。

**Methods**：我们使用 Claude Opus 4.6（9 配置 × 15 任务 × 3 重复 = 405）与 GPT-5.4（81 份用于跨模型验证）共生成 486 份 QMS 文件，涵盖 4 个 prompt 内容维度（规则、文档骨架、详细内容、worked examples；0–56,000 tokens）。合规性按 0–5 Likert 量纲在三层框架下评分：自动化规则式评分器；双 LLM-as-judge 评审（864 条评分）；以及 3 位 ISO 15189 资格内审员对 10 份分层抽样文件的盲法评审。消融效应采用 Mann–Whitney U 检验配合 BH 校正与 bootstrap 95% CI；评审员一致性采用 ICC 变体。

**Results**：在 LLM 评审层，仅规则成分产生显著合规增益（Δ=+0.511；BH-adjusted p<0.001）。C_full（~56,000 tokens）在 Claude 下评分 3.22–4.56，在 GPT-5.4 下仅 1.40–1.84。两位 LLM 评审均将 Claude 生成输出评得比 GPT 生成高约 0.30 分（Panickssery：Claude +0.29，GPT −0.30），集中表现于 C_full 且与经典自偏好不兼容。专家间一致性极佳 [ICC(2,k)=0.982]；Claude 评审与专家一致性中等 [ICC(3,1)=0.548]，GPT 评审较差 [ICC(3,1)=0.217]；两位 LLM 评审均把专家评分高估 0.52–0.90 分。LLM 偏好的 H4_sop_only（~2,000 tokens）在专家评估下跌至 7 配置中的第 5 名（3.20），而模板锚定的 F_template、H2_keep_examples 与 G_template_rules 排名最高（4.06–4.24）。

**Conclusions**：最优配置取决于评估层：极简 prompt（~1,000–2,000 tokens）适用于探索性草稿；模板锚定 prompt（~15,000–16,000 tokens）对认可级文件属必需；C_full（~56,000 tokens）在 GPT-5.4 下避免使用。LLM-as-judge 可作首道筛选；专家终审仍属必需。

---

## 1. Introduction

ISO 15189:2022《医学实验室——质量和能力的要求》[7] 是医学实验室认可的国际标准，且其在中国医学实验室的采用在中国合格评定国家认可委员会（CNAS）框架下持续扩大 [14]。对应的国内实施文本 CNAS-CL02:2023 同期发布。该类标准规定实验室必须达到何种要求，而不规定如何达到，因此每家实验室须自主构建一套独立的质量管理体系（quality management system, QMS）文件集，包含质量手册、程序文件与作业指导书。根据通讯作者作为 ISO 15189 内审员的经验，此类体系在典型三级甲等医院检验科中通常包含 100–300 份受控文件，涉及结构组织、条款–文件映射、表单编号与职责分配；由内部质量小组手工编写通常需时数月，再经多轮内部审核方可定型。寻求 CNAS 认可的实验室通常会聘请外部技术专家或培训师协助完成此过程。

大语言模型（LLM）的发展为这一工作量的实质性自动化带来了可能。Claude Opus 4.6 与 GPT-5.4 等前沿模型在长文档生成、结构化输出与领域专业术语使用方面已显示出相应能力 [1, 2]，且 LLM 已被应用于科学研究 [8] 与医学问答 [9]。然而，何种 system prompt 设计能够生成合规且具备可操作性的 QMS 文件，尚未得到系统性研究。实践中已出现两种对立的做法：其一为全量上下文做法，将所有可能相关的材料——ISO 标准原文、CNAS 准则、既有文件库与 worked examples——一并载入 system prompt，常超过 50,000–100,000 tokens；其二为极简 prompt 做法，仅提供规则约束与章节骨架，依赖模型内化知识完成内容生成，prompt 长度被限制在数千 token 以内。支持任一做法的实证证据均有限，因为现有 LLM 行为与 prompting 综述 [4, 12] 多关注通用任务，并未系统比较 QMS 撰写这类专业监管文档场景。

第二个、更根本的问题涉及评估方法学本身。LLM 生成的输出当前最常见的评估方式是 LLM-as-judge 范式，即由另一个 LLM 担任评分者 [5]。长文本生成评估 [10] 与大规模人类偏好基准 [11] 已成为该文献中两种主要的评估范式。已有工作记录到 LLM 评审倾向于呈现 self-preference bias，偏好同家族模型生成的输出 [6]。然而，该偏差是否以及如何在医学实验室 QMS 等专业监管领域中表现、以及它如何传播到配置比较结论中，尚未得到实证刻画。

为弥补上述空白，本研究生成了 486 份 QMS 文件、收集了 864 条 LLM 评审评分、并获得了 30 条盲法专家评分，以探究以下研究问题：(i) system prompt 配置中的哪些成分——规则、文档骨架、详细内容、worked examples——对 LLM 生成 QMS 文件的合规性贡献最大？(ii) 最精简的有效 token 预算是多少？(iii) 最优配置是否在生成模型之间（Claude Opus 4.6 与 GPT-5.4）一致？(iv) 在本研究领域 LLM 评审 self-preference bias 的量级如何？(v) 在结合自动评分、LLM 评审与专家评分的多层次评估框架下，哪种配置最稳健？

---

## 2. Materials and methods

### 2.1 配置组设计

基于规则、文档骨架、详细内容、worked examples 四个 prompt 内容维度的系统替换，按各维度操作定义的水平变化（规则与文档骨架为三水平：缺失 / 部分 / 完整；详细内容与 worked examples 为二水平：缺失 / 存在），设计 9 组 prompt 配置（Figure 1）。两组极简配置作为基线：A_bare（0 tokens；无 system prompt）与 B_simple（~300 tokens；含语言、文件结构、标准引用、术语、表达风格与编号 6 条编号约束的简短任务指令——编码为规则维度的 partial 水平）。C_full（~56,000 tokens）代表全量上下文输入策略，由实验室简介与全部 SOP 串接组成单一上下文块；由于未单独提供独立的强制性规则块，C_full 同样编码为规则维度的 partial 水平。E_rules_v2（~1,200 tokens）仅含规则成分；F_template（~15,000 tokens）为无规则的完整文档模板；G_template_rules（~16,000 tokens）为规则与模板的组合；H2_keep_examples（~25,000 tokens）在 G_template_rules 基础上扩展 worked examples；H3_skeleton（~5,000 tokens）保留模块骨架但删除详细内容；H4_sop_only（~2,000 tokens）仅保留与请求任务最相关的单个 SOP 骨架。字母 D 在编号序列中被有意跳过：早期 D_rules 变体经专家验证发现术语错误后被弃用，由 E_rules_v2 替代；保留字母跳号以保持配置标识符的时间一致性。

![Figure 1](figures/fig1_config_composition.png)

**Figure 1.** 本研究评估的 9 个 prompt 配置。左面板：各配置在 4 个 prompt 内容维度（规则、文档骨架、详细内容、示例）上的纳入情况；✓ = 完整纳入，◐ = 部分纳入，— = 缺失。右面板：每个配置的总 system-prompt 体量，以千 token 为单位（cl100k_base tokenizer）。

规则成分基于经过整理的 `rules.md` 文件（~1,200 tokens），并经领域专家校验精修。删除 3 条错误术语映射（仪器 → 设备；校准品 → 校准物；室间质评 → 能力验证），修正 3 条目标术语（标本 → 样品；检验项目 → 检测项目；线性范围 → 可报告范围）；箭头表示「非首选 → ISO 15189 首选」方向。最终规则集保留 10 条经验证的术语映射与 7 类被禁的模糊表述。文档骨架由自定义 *strip_to_skeleton* 算法从机构模板库中提取，保留章节标题、各章节首段说明与表单编号方案，删除条款原文摘录、详细表格内容、worked examples、step-by-step 程序与 fenced code blocks（markdown ```...``` 构造，含流程图、JSON 片段或伪代码）。

本研究所有报告的 token 数均使用 cl100k_base tokenizer（OpenAI tiktoken 库）计算；在中英混合医学文本上，该 tokenizer 与 Anthropic 原生 tokenizer 通常相差 ≤10%，作为可重复的近似估计。

### 2.2 生成模型与任务

主实验采用 Claude Opus 4.6（Anthropic，美国加州 San Francisco），通过 Claude Code Agent 接口（Anthropic 的命令行 agent 框架）以文本生成模式运行：sub-agent 仅返回文本回复，文件生成阶段未发生任何 agentic 工具调用（文件系统、网络访问、代码执行），但 Claude Code 框架自带的工具定义始终存在于 framework 级 system prompt 中（详见 §4.5 局限性 xiii）。模型测试跨越 9 组 prompt 配置、15 项 QMS 编写任务、每元胞 3 次独立重复，共生成 405 份文件。15 项任务按 CNAS 评审场景分层为三类，每类 5 项：A 类（文件编写，例如人员培训与能力评估控制程序）、B 类（体系运行，例如年度内审检查表）、C 类（审核模拟，例如内部质控程序文件审查报告）。完整任务列表与原始 prompt 已公开于 GitHub 仓库 `task_messages/` 与 `configs/` 目录。跨模型验证采用 GPT-5.4（OpenAI，美国加州 San Francisco），通过官方 openai Python SDK（v2.30.0）调用，base URL 配置为 AIHubMix 端点（https://aihubmix.com）；采用此路由是因研究期间作者所在地区无法直接访问 OpenAI API。（输出目录沿用早期脚本迭代时的 `gpt4o_*` 前缀命名，所有调用的实际运行 model 均为 GPT-5.4，由 SDK `model` 参数传入。）GPT-5.4 在相同 9 组配置下评估，每类各取一个代表性任务（A1、B1、C1，定义为各类按索引的第一个任务），3 次重复，共生成 81 份文件。两模型在每个实验元胞内接收完全相同的 system prompt 配置，并使用完全相同的生成参数：temperature = 1.0、max_tokens = 12,000；所有其他生成参数采用模型默认值。较高的采样温度选择是为反映真实交互使用场景；为捕捉由此引入的随机性方差，每元胞设 3 次独立重复。所有 API 调用执行于 2026 年 4 月 2 日至 4 月 14 日之间。

### 2.3 三层评估框架

合规性通过互补的三层框架进行评估：基于规则的自动评分器（Tier 1）、双 LLM-as-judge 评审（Tier 2a 与 2b）、独立盲化专家评审（Tier 3）。三个层次的评分均使用统一的 0–5 整数尺度；Tier 1 采用为可由代码可靠检测的特征定制的算法量规，而 Tier 2 与 Tier 3 共用 Table 1 定义的描述性五维度量规。

#### 2.3.1 Tier 1 — 自动合规评分

Python 自动合规评分器（`auto_scorer.py`，已开源；详见 Data availability）对全部 486 份文件按**三个主要维度**评分，并合成为加权综合分。

**格式**：按任务类别匹配必需章节标题（A 类程序文件 8 段；B 类检查表/报告 6 段；C 类审查报告 7 段；接受常见同义变体），结合编号层级深度与空章节检测。缺失 ≥3 段记 1 分，缺失恰好 1 段记 3 分。

**条款覆盖**：正则匹配 ISO 15189:2022 第 4–8 章条款号（如 5.4.1），用前后 40 字符上下文窗口过滤误匹配。引用 ≥10 个独立条款且至少 1 处引用 CNAS-CL02:2023 记 5 分；无标准引用记 1 分。

**术语合规**：本维度内部聚合两类互补检查。(i) *术语映射*：基于 ISO 15189:2022 / CNAS-CL02:2023 校验的 14 条术语对照表（如"分析前过程"→"检验前过程"、"标本"→"样品"、"不确定度"→"测量不确定度"），并配合上下文排除规则避免合理用法误判（例如"测量不确定度"中的"不确定度"不计违规）。(ii) *模糊表述检测*：检测低质量 QMS 文稿中常见的模糊词，如"及时"、"相关人员"、"定期"，经复合词白名单与后续 30 字符内频率量化（如出现"每周"、"每年"则不计）双重过滤。

**综合分**：三个测量维度按 `auto_scorer.py` 中 `WEIGHTS` 字典定义的权重合成为加权综合分（`auto_weighted`）：格式 = 0.18、条款覆盖 = 0.22、术语 = 0.13——这是该字典所列七个权重项中已实现的三项。字典中其余四项（逻辑一致性 = 0.18、可操作性 = 0.10、安全合规性 = 0.09、人工修改量 = 0.10；合计 0.47）为早期 7 维评分方案的残留条目，已被 §2.3 所述三级评估框架取代；这四项**未纳入 `auto_weighted` 计算**，因此不参与 Tier 1 排序。三个已实现权重合计为 0.53，故 `auto_weighted` 在 0–5 评分尺度下的理论范围为 [0, 2.65]。此非单位权重总和仅为评分尺度的表面特征：将每个权重乘以 1/0.53 以归一化至单位和（格式、条款覆盖、术语分别约为 0.34、0.42、0.25），仅是 `auto_weighted` 的正线性变换，因此既保留各配置组的均值排序，亦保留 §3.1 用于构建综合排序的 min-max 归一化结果（Spearman ρ = 1.00，由变换形式必然成立）。§3 报告的所有 Tier 1 排序对采用原始权重抑或归一化后的单位和权重均完全一致。

#### 2.3.2 Tier 2 — LLM-as-judge

两位 LLM 评审员部署于 2 × 2 对称跨模型设计——Claude-生成 × Claude-judge、Claude-生成 × GPT-judge、GPT-生成 × Claude-judge、GPT-生成 × GPT-judge——以正交分解自评偏差。

**Tier 2a（Claude-as-judge）**：Claude Opus 4.6 以"CNAS 主任评审员"角色 prompt（即 `gpt_cnas_judge.py` 中定义的 `JUDGE_PROMPT_TEMPLATE`，与 Tier 2b 完全一致）对每份文件按五维度量规（Table 1）以 0–5 分评分。生成参数：temperature = 1.0、max_tokens = 4,096；每份文件经单次 API 调用得到 1 次评分。共生成 378 条 Claude-judge 评分，分布如下：270 条覆盖 6 个核心配置（A_bare、B_simple、C_full、E_rules_v2、F_template、G_template_rules）× 15 任务 × 3 重复的 Claude-生成文件（每篇 raw JSON 完整公开）；81 条覆盖全部 9 配置 × A1/B1/C1 × 3 重复的 GPT-生成文件（仅以聚合均值归档，详见 §4.5 局限性 x）；27 条覆盖 H 组配置（H2_keep_examples、H3_skeleton、H4_sop_only）× A1/B1/C1 × 3 重复的 Claude-生成文件（同样仅以聚合均值归档）。

**Tier 2b（GPT-as-judge）**：GPT-5.4，按 §2.2 所述通过 AIHubMix 端点接入，使用与 Tier 2a 完全相同的 prompt、量规与 0–5 分评分尺度，生成参数同样为 temperature = 1.0、max_tokens = 4,096。全部 486 份生成文件均被评分（405 Claude-生成 + 81 GPT-生成），每份 1 次评分；per-paper raw JSON 完整保留并公开。已验证 max_tokens 上限未导致评审输出截断：486 份 GPT-judge per-paper JSON 全部成功解析（0 解析错误），且两位评审员的 per-dimension `reason` 字段最长为 43 字符，仍处于 prompt 所设的40 字软上限内，远低于 4,096 token 的输出预算。

合计 Tier 2a 与 2b 共得 864 条 LLM 评审评分（378 条 Claude-judge + 486 条 GPT-judge）。非对称的评分数反映 Claude 评审未覆盖 H 组完整 15 任务子集及完整 GPT-生成集（详见 §4.5 局限性 x）；关键的是，所有 4 个 2 × 2 象限均有评分填充（部分仅以聚合均值形式，详见 §4.5 局限性 x），保证自评偏差分解可在 cell 均值层面进行。

**评分尺度**：每个维度按 0–5 整数评分：5 = 完全符合（Table 1 的 5 分锚点）；4 = 基本符合（介于 5 分与 3 分锚点之间，仅有少量瑕疵）；3 = 部分符合（3 分锚点）；2 = 明显不符（介于 3 分与 1 分锚点之间）；1 = 严重不符（1 分锚点）；0 = 维度不可评估——文件实质性缺失或非实质性输出（例如模型仅返回计划性问询而未生成所需文件）。下表 5/3/1 分锚点描述以完全相同的措辞同时提供给所有评审员（LLM 与人类专家）；中间分数（2、4）由评分员在两个相邻锚点之间判定。

**Table 1.** Tier 2a/2b 与 Tier 3 共用的五维度描述性量规。

| 维度 | 5 分锚点 | 3 分锚点 | 1 分锚点 |
|------|----------|----------|----------|
| 条款满足度 | 对应条款所有 SHALL 要求均有具体落地措施 | 覆盖主要条款但有遗漏或浮于表面 | 大量条款仅引用未落实，或严重遗漏 |
| 可操作性 | 每步有具体责任人（岗位名）、量化时限、明确输出（表单编号） | 大部分步骤可操作，少量模糊 | 大量"及时""相关人员""定期"等无法执行的表述 |
| 内部一致性 | 引用的文件/表单全部在相关章节列出，职责分配清晰 | 少量悬空引用或表述矛盾 | 大量悬空引用或职责冲突 |
| PDCA 闭环 | 明确有计划、执行记录、效果评估、不合格处理→改进的完整链条 | 有 P-D-C 但缺少 A（改进/反馈机制） | 仅描述执行步骤，无检查和改进 |
| 专业深度 | 包含检验科专业细节（如 Westgard 规则、测量不确定度、Sigma 度量、HIL 指数、盲样测试、PCR 分区、冷链等） | 有一定专业性但偏通用 | 内容泛泛，可套用于任何实验室 |

#### 2.3.3 Tier 3 — 专家评审

3 位 ISO 15189 资格内审员对 10 份盲化、分层随机抽样的文件进行独立评分，采用与 LLM 评审员完全相同的五维度量规（Table 1）。Rater 1 为第一作者，本身为合格 ISO 15189 内审员；Rater 2 与 Rater 3 为同单位合格 ISO 15189 内审员。为最小化自我影响，Rater 1 在完成评分前未查看任何 Tier 1 或 Tier 2 评分输出；Rater 1 仅在三位评分员的评分表全部提交后方查阅抽样文件的 Tier 1/2 输出。三位评分员独立评分且互不交流；Rater 2 与 Rater 3 在不知晓 Rater 1 评分的情况下完成评分，三组评分仅在所有提交完成后才合并。Rater 2 与 Rater 3 在评分前已获得书面知情同意。评分过程中，专家可自由查阅 ISO 15189:2022 与 CNAS-CL02:2023 的完整正文及附录。

**抽样策略**：从 486 份文件池中以分层随机抽样方式抽取 10 份，采用固定 Python 随机种子（`seed = 42`），按 7 个配置 × A 类程序文件任务（A1、A2、A3）分层——构成 21 层抽样框。本层抽样所选用的 7 个配置（A_bare、C_full、E_rules_v2、F_template、G_template_rules、H2_keep_examples、H4_sop_only）与 Tier 2a（§2.3.2）的"6 核心配置"集合不同：B_simple 在专家样本中作为冗余的低质量基线（与 A_bare 重复）被排除，H3_skeleton 因在每层样本规模下与 H4_sop_only 高度重复而被排除，H2_keep_examples 与 H4_sop_only 则作为 H 系列的两个端点被纳入。抽样规模选 10 是为平衡专家工作量与分层覆盖；最终样本未覆盖全部 21 层（每个被抽中的层取 1–2 份）。选择 A 类是因为其在 CNAS 评审中是最稳定且最具评审相关性的文件类型；跨类别的可推广性已在 §4.5 中作为局限性予以说明。

**评分员利益冲突声明**：3 位评分员均与 Anthropic、OpenAI 及其他 LLM 提供商无商业、科研或咨询关系；本研究亦未接受上述机构的资金或实物资助。

**评分前校准**：本研究未开展正式的评分前校准会议；3 位评分员仅依据公布的五维度量规（Table 1）与 ISO 15189:2022 / CNAS-CL02:2023 标准独立评分。校准缺失作为方法学局限已在 §4.5 (xii) 中说明。

**盲法实施程序**：盲法按 4 层实施（脚本 `prepare_blind_review.py`，已开源）：

(i) *文件重命名*：每份抽样文件从原路径 `outputs/{group}/{group}-{task}-{rep}.md` 复制到扁平化匿名序列 `paper_01.md … paper_10.md`，文件名与目录结构均去除组名与重复编号。

(ii) *正文去标识自检*：自动文本扫描确认 10 份盲化文件正文中无任何模型标识（"Claude"、"GPT"、"Opus"）或配置组关键词（"H4"、"C_full"、"G_template"、"F_template"、"H2_keep"、"E_rules_v2"、"A_bare"、"H3_skeleton"），保证模型与配置来源无法从正文推断。

(iii) *顺序随机化*：原（group, task, rep）三元组到 `paper_01`–`paper_10` 的分配采用固定 Python 随机种子（`seed = 42`）打乱；三位专家看到的呈现顺序完全相同。评分表中仅披露任务类别（如"人员培训与能力评估控制程序"），因其为文件内容固有属性且评分所需；底层配置组仍被隐藏。

(iv) *key 隔离*：（paper_id → group, task, replicate）映射文件 `blind_review/key.json` 在评分前封存，三位专家评分表全部提交后方开启。
### 2.4 统计方法

#### 2.4.1 组间成对比较与多重校正

组间成对比较采用双侧 Mann–Whitney U 检验（`scipy.stats.mannwhitneyu`，scipy v1.10.1），针对 per-document GPT 评审评分，每个配置贡献 n = 45 条评分（15 任务 × 3 重复）。四成分消融的多重比较校正采用 Benjamini–Hochberg 错误发现率（FDR）方法（`statsmodels.stats.multitest.multipletests`（statsmodels v0.14.6），method = `fdr_bh`，α = 0.05）。选用 FDR 而非 Bonferroni 校正，是因为四个预设对比之间存在配置重叠（例如 G_template_rules 同时出现于 *detailed content* 与 *worked examples* 两个对比），统计上并不独立；在此类结构化测试中，Benjamini–Hochberg 方法在严格控制错误发现期望比例的同时提供更高的统计功效。每个 Δ 效应估计的 95% bootstrap 置信区间采用非参数 percentile 方法计算：固定种子 42，对每组独立有放回重采样（numpy `random.choice`）共 B = 10,000 次，区间下/上限取重采样 Δ 分布的 2.5th/97.5th 百分位；bootstrap 参考实现见已发布代码仓库的 `bootstrap_ci.py`。

#### 2.4.2 配置成分效应的量化

4 个配置成分效应通过靶向成对对比定义，每个对比设计为隔离一个维度，同时尽量保持其他三个维度恒定：

- *rules*（规则）：E_rules_v2 vs A_bare
- *document skeleton*（文档骨架）：H4_sop_only vs E_rules_v2
- *detailed content*（详细内容）：G_template_rules vs H3_skeleton
- *worked examples*（示例）：H2_keep_examples vs G_template_rules

每个对比的效应量 Δ 定义为简单算术均值差，Δ = mean(组 B) − mean(组 A)，其中各组均值为该配置下 45 条 per-document GPT 评审评分的非加权算术平均。未加入任何协变量、随机效应、加权或收缩。同一份每组 45 个样本同时作为对应 Mann–Whitney U 检验的输入。本研究未采用 L9 正交表分解、最小二乘均值（least-squares means）或混合效应模型，因为靶向对比方案对所关注的替换型对比给出更透明、更可直接解读的估计。

#### 2.4.3 评分者间一致性

评分者间一致性采用三类互补指标进行评估，全部完整报告，因其各自捕捉一致性的不同侧面：Pearson 相关系数捕捉线性关联同时容许评分者间系统性偏移；Spearman 相关系数捕捉排序一致性而不假设线性；组内相关系数（ICC）按 Shrout 与 Fleiss [13] 的标准框架定量信度。所采用的 4 种 ICC 变体如下：

- **ICC(2,1)** — 单评分者绝对一致性，双向随机效应；
- **ICC(3,1)** — 单评分者排序一致性，双向混合效应；
- **ICC(2,k)** — k 评分者平均绝对一致性；
- **ICC(3,k)** — k 评分者平均排序一致性。

单评分者变体 ICC(2,1) 与 ICC(3,1) 用于两两比较（如专家均值 vs 各 LLM 评审，及专家组内两两比较）；k 评分者均值变体 ICC(2,k) 与 ICC(3,k)（k = 3）用于评估三专家组的整体信度。所有 ICC 计算采用 `pingouin` Python 库（v0.6.1）。

#### 2.4.4 自评偏差

对于每个作为评审员的模型 M ∈ {Claude Opus 4.6, GPT-5.4}，自评偏差按 Panickssery 等 [6] 的经典定义计算——同一评审员、不同生成者：

bias_M = mean(judge = M, generator = M) − mean(judge = M, generator = M′)，

其中 M′ 为另一模型。正值表示评审员 M 对自家模型族生成的输出评分高于对手生成者；负值反之。作为敏感性检验，我们另以替代的跨评审公式（同一生成者、不同评审员：bias_M = mean(judge = M, generator = M) − mean(judge = M′, generator = M)）重新计算，得到 Claude +0.464、GPT −0.472，与 §3.4 报告的经典值（+0.294 与 −0.301）方向一致。

#### 2.4.5 实验设计说明

本研究的 9 个评估配置并非 Taguchi L9 正交表，而是 4 维配置空间（规则 / 文档骨架 / 详细内容 / 示例）的结构化子集；各维度按其操作定义所相关的水平变化：**规则与文档骨架为三水平（缺失 / 部分 / 完整）**，**详细内容与示例为二水平（缺失 / 存在）**。配置选取目的是通过 §2.4.2 列出的靶向成对对比隔离每个维度的影响，而非满足 L9 设计的正交平衡要求。因此 Δ 效应估计仅对应 §2.4.2 中列出的特定配置对，未对完整因子设计参考做加权重映射。

---

## 3. Results

### 3.1 配置在自动评分与 LLM 评审下的综合排名

在 Claude Opus 4.6 生成的 405 份文件中，9 个配置按综合分排名，该综合分由 Tier 1 自动评分均值与 Tier 2 LLM 评审均值（跨 Claude、GPT 两位判官取均值）合成：每项分别在 9 组上做 min-max 归一化至 [0, 1]，再以等权平均。从高到低，排名结果为：H4_sop_only（~2,000 tokens；0.994）、H3_skeleton（~5,000 tokens；0.869）、G_template_rules（~16,000 tokens；0.851）、H2_keep_examples（~25,000 tokens；0.759）、E_rules_v2（~1,200 tokens；0.729）、C_full（~56,000 tokens；0.493）、F_template（~15,000 tokens；0.345）、B_simple（~300 tokens；0.227）、A_bare（0 tokens；0.000）。H4_sop_only 仅以 ~2,000 tokens 获得最高综合分——远低于模板锚定配置（G_template_rules ~16,000；H2_keep_examples ~25,000）与全量 C_full（~56,000）；但如 §3.5 所示，该结论在专家层未能保持。

### 3.2 四成分替换对比消融

4 个消融效应同时报告 raw p 值、Benjamini–Hochberg 校正 p 值与 95% bootstrap 置信区间（B = 10,000 次重采样；seed = 42）。规则成分是 4 个成分中唯一在校正后仍达到显著的主效应（Δ=+0.511；95% CI [+0.28, +0.75]；raw p<0.001；BH-adjusted p<0.001）。文档骨架成分（Δ=+0.213；95% CI [+0.05, +0.39]；raw p=0.055；BH-adjusted p=0.11）方向为正；虽 bootstrap CI 不含 0，但 BH-adjusted p 未达 0.05 阈值。该不一致源于 CI 基于简单均值差计算，而推断采用基于秩的 Mann–Whitney U 检验；本研究将骨架效应视为提示性证据，需通过独立重复实验进一步验证。详细内容（G_template_rules vs H3_skeleton：Δ=−0.031；95% CI [−0.19, +0.12]；raw p=0.79；BH-adjusted p=0.79）与示例（H2_keep_examples vs G_template_rules：Δ=−0.053；95% CI [−0.21, +0.11]；raw p=0.46；BH-adjusted p=0.61）无可检测贡献。作为四成分 BH 集合外的描述性补充对比，H4_sop_only 与 H3_skeleton 差异不显著（Δ=−0.009；raw p=0.80；未做校正报告），提示在 LLM 评审层下，任务特定的 SOP 骨架（~2,000 tokens）与完整模块骨架（~5,000 tokens）功能等效。本节所报告的消融结果仅适用于 LLM 评审层（具体为 §2.4.1 所述的 Tier 2b GPT 评审评分）；对应的专家层比较见 §3.5。

### 3.3 2×2 跨模型对称验证

Figure 2 展示 2×2 对称设计——Claude 生成 × Claude 评审、Claude 生成 × GPT 评审、GPT 生成 × Claude 评审、GPT 生成 × GPT 评审——评估于 9 组配置 × 3 个代表任务（A1、B1、C1）× 每单元 3 次重复。全量上下文配置 C_full（~56,000 tokens）在 GPT-5.4 生成条件下合规分出现显著下降：GPT-gen × Claude-judge 均值为 1.40，GPT-gen × GPT-judge 均值为 1.84（0–5 Likert 量纲），而同一 C_full 配置在 Claude Opus 4.6 生成条件下两位判官的跨评估均值落在 3.22–4.56 区间。该模式表明 ~56,000-token 全量上下文配置的表观可用性局限于 Claude Opus 4.6，在本研究测试的参数下无法推广至 GPT-5.4。作者对 GPT 生成的 C_full 输出进行了定性检视，识别出三类反复出现的失败模式：（i）指令遵循衰退，即 system prompt 早期声明的约束在输出后段不再得到体现；（ii）结构错乱，表现为章节顺序不一致、必需标题缺失或编号错误；以及（iii）条款引用混淆，包括使用错误、不匹配或捏造的 ISO 15189:2022 条款编号。在相应的 Claude Opus 4.6 输出中未观察到这些失败模式。

![Figure 2](figures/fig2_2x2_symmetric.png)

**Figure 2.** 2 × 2 跨模型对称设计的热力图。单元格显示 9 个配置（行）× 4 个生成器–评审员组合（列）下，跨 3 个代表性任务（A1、B1、C1）的平均合规分数（0–5 Likert 量纲）。C_full 在 GPT 生成的两列（1.40 与 1.84，黑框标注）出现显著下滑，与 Claude 生成的两列形成鲜明对比（Claude 评审 × Claude 生成 = 4.56；GPT 评审 × Claude 生成 = 3.22）。

### 3.4 LLM 评审的自评偏差

依 §2.4.4 定义的 Panickssery 经典公式（bias_M = mean(judge = M, generator = M) − mean(judge = M, generator = M′)）计算，Claude 评审在 9 组配置上的均值偏差为 +0.294（0–5 Likert 量纲；6 组正向，单组最大值 +3.156 出现于 C_full）。GPT 评审均值偏差为 −0.301（6 组负向，A_bare 与 B_simple 为正，F_template 为零）。两位判官在方向上达成一致——跨 9 组配置，两者实际上均把 Claude 生成输出评得比 GPT 生成高约 0.30 分，尽管自评偏差指标的符号在表面上相反。将 C_full 作为主要离群点排除后，Claude 评审均值偏差衰减至 −0.064（9 配置中位数：+0.200），GPT 评审均值偏差衰减至 −0.167（中位数：−0.311），表明上述 Panickssery 指数主要由 C_full 拖动，其长上下文失败模式（§3.3）在该处放大了跨判官分歧。

按定义，该符号相反的模式与"经典自评偏差"（每位判官各自偏好自家生成）不兼容——后者应表现为两位判官均为同号正值。所观察到的模式与两种非互斥假设相容：(a) 在本研究参数设置下，Claude Opus 4.6 与 GPT-5.4 之间存在真实的生成质量差异，与 §3.3 报告的 GPT-5.4 在 C_full 下的崩盘模式一致；(b) 两位判官共享的风格或格式偏好倾向于 Claude 生成的表达形式。由于 Tier 3 专家样本（n=10）全部抽取自 Claude 生成集（§2.3.3），本研究无法在经验上判别上述两种解释；我们将此识别为后续验证研究的关键方向（§4.5 局限性 i）。

为考察去除同判官自评后的配置排序，我们仅使用跨模型评分（每个配置保留 Claude 评审 → GPT 生成、与 GPT 评审 → Claude 生成的 per-document 均值，再两两取均值）重新排序。在此去偏排序下，前四配置在 0–5 Likert 量纲上的均值分别为：G_template_rules（4.211）、H3_skeleton（4.167）、E_rules_v2（4.133）、H4_sop_only（4.100）；四者间最大成对差为 Δ=0.111，统计上不可区分。C_full 由 §3.1 综合排序的第 6 名跌至第 9 名（均值=2.310），表明 C_full 在 §3.1 中获得的较高 LLM 评分主要由两点驱动：Claude 评审对自家输出的高估、以及 GPT-5.4 在 ~56,000 token 配置下无法产生可用输出（§3.3）。

### 3.5 专家层校验

3 位专家间一致性极高：ICC(2,k)=0.982（95% CI [0.95, 1.00]）；ICC(3,k)=0.981。两两单评分员一致性 ICC(2,1) 分别为 0.948（R1 vs R2）、0.928（R1 vs R3）、0.969（R2 vs R3），均位于"优秀"区间（>0.90，按 Cicchetti 标准 [15]）。该一致性水平表明 5 维度评分量规（Table 1）在评分员间高度可重复；然而由于三位评分员均来自同一单位，所观察到的可靠性可能高估跨单位一致性（见 §4.5 局限性 ii）。

专家均值与两位 LLM 评审之间的一致性显著低于专家间（Figure 3）。Claude 评审 ICC(3,1)=0.548（p=0.04），Pearson r=0.573，Spearman ρ=0.509；GPT 评审 ICC(3,1)=0.217（p=0.26），Pearson r=0.259。在 0–5 Likert 量纲下，两位 LLM 评审均系统性高估专家所给的合规分数：Claude 评审高估 0.905 分，GPT 评审高估 0.525 分（mean difference 定义为 expert − LLM judge，分别为 −0.905 与 −0.525）。Claude–专家一致性达中等水平，GPT–专家一致性较差。

![Figure 3](figures/fig3_expert_vs_llm.png)

**Figure 3.** LLM 评审相对 3 位专家小组对合规分数的系统性高估（n = 10 文档 × 3 位评分员）。横轴：3 位专家的均值评分。纵轴：LLM 评审评分。左：Claude Opus 4.6 作为评审 [ICC(3,1) = 0.548；Pearson r = 0.573；mean difference (expert − Claude) = −0.905]。右：GPT-5.4 作为评审 [ICC(3,1) = 0.217；Pearson r = 0.259；mean difference (expert − GPT) = −0.525]。虚线：1:1 完全一致。标记按配置着色（图例插入）。

按专家均值对所抽样的 7 个配置（共 10 份文件；每层 n=1 或 2）排序为：F_template 4.24（n=1）、H2_keep_examples 4.07（n=1）、G_template_rules 4.06（n=2）、C_full 3.45（n=2）、H4_sop_only 3.20（n=2）、E_rules_v2 3.19（n=1）、A_bare 3.04（n=1）。LLM 评估层第 1 名的配置——H4_sop_only（~2,000 tokens）——在专家视角下跌至第 5/7 名（倒数第三），仅高于空 prompt 基线 A_bare 0.16 分。LLM 评审对 C_full 与 H4_sop_only 高估最严重（mean difference = expert − LLM-judges mean，分别为 −1.00 与 −1.05），提示这两种配置虽呈现结构完整性与术语合规性（自动评分与 LLM 评审最易捕获的维度），但缺乏只有专家评审才能察觉的临床实操深度。专家排序前三的配置（F_template、H2_keep_examples、G_template_rules）均为含详细内容的模板锚定配置，表明在 LLM 评审层呈现的"骨架配置 token 效率优势"并不能转化为专家可验证的合规性。考虑到每层样本极小（n=1 或 2），上述专家排序应视为探索性结论，需通过更大规模专家样本进行重复验证。

### 3.6 Token 规模与合规分数：跨评估层的差异关系

Figure 4 以三位评估者的视角呈现 compliance 分数与 system-prompt token 规模的关系，三条曲线均基于 n=10 的专家盲评子集（7 个配置；每层 n=1 或 2）。在 LLM 评审层下，Claude 评审曲线整体随 token 规模上升，于 C_full（~56,000 tokens）达峰值 4.90，但在 H2_keep_examples 处出现一个小回落；GPT 评审曲线在 G_template_rules（~16,000 tokens）达峰值 4.50，在 token 范围两端（包括 C_full）相对平坦于 ~4.0。在专家层下，曲线在模板区达峰值（F_template 4.24（~15,000 tokens）；G_template_rules 4.06（~16,000 tokens）），在两端均下滑——H4_sop_only（~2,000 tokens）跌至约 3.20，C_full（~56,000 tokens）跌至 3.45。专家–LLM 评审之间的分歧呈 U 型分布：在低 token 端配置（A_bare、E_rules_v2、H4_sop_only）gap 达 0.8–1.1 分，在 token 高端（C_full）gap ≈ 1.0；中间 ~15,000–25,000-token 模板区收敛（gap ≤ 0.6）。两条 LLM 评审曲线均把低 token 区置于模板区附近或之上，而专家曲线则把模板区明显置于所有其它配置之上。此模式表明 token 效率导向优化与临床可用性导向优化在医学实验室 QMS 生成场景中对应两个差异的优化目标；Tier 2 LLM 评审视角同时高估了短 prompt 配置与 C_full 配置的质量，相对于专家层所验证的真实合规性而言。

![Figure 4](figures/fig4_token_vs_quality.png)

**Figure 4.** Compliance 分数（0–5 Likert）与 system-prompt token 体量的关系，基于 n = 10 专家盲评子集计算（7 个配置；每层 n = 1 或 2）。横轴：token 数，对称对数刻度（cl100k_base tokenizer）。三条曲线均基于同一组匹配样本：绿色实线（方块）为 3 位专家均值；红色实线（圆点）为 Claude Opus 4.6 评审应用于 Claude 生成输出；蓝色实线（三角）为 GPT-5.4 评审应用于 Claude 生成输出。橙色阴影带：LLM 评审层识别的 token 高效最优区（H4_sop_only / H3_skeleton）。绿色阴影带：专家评估识别的临床可用性最优区（F_template / G_template_rules）。因每层 n = 1 或 2，未绘制误差棒；对应的 LLM 与专家校准散点见 Figure 3。

---

## 4. Discussion

### 4.1 Prompt 精简化在 LLM 评审层成立但在专家层不成立

四成分消融在 LLM 评审层下支持一个简洁论断：规则成分必需（BH-adjusted p < 0.001），文档骨架成分方向为正但未达显著（BH-adjusted p = 0.11），详细内容与示例均未产生可检测的合规增益（§3.2）。此模式与 Liu 等 [3] 描述的 lost-in-the-middle 现象一致——即在长 prompt 中追加大量上下文材料可能稀释模型注意力并降低输出质量——亦与更广义的 prompt-engineering 文献相符 [12]。

专家层分析对该简洁论断进行了限定（§3.5）。详细内容——F_template 与 G_template_rules 中嵌入的完整文档模板——与显著更高的专家合规评分相关：在 0–5 Likert 量纲下，F_template 评分 4.24（n=1）、G_template_rules 评分 4.06（n=2），而 H4_sop_only 仅 3.20（n=2），表观差距约 1 分（每层样本极小，应视为探索性观察；详见 §3.5）。一个可能的解释是，模型内化的知识并不能可靠覆盖 ISO 15189:2022 与 CNAS-CL02:2023 所要求的临床实操子场景——在本研究任务集合中，包括急诊样本处理、患者自采标本的接收、样本运送人员的资格要求、以及详细的样本拒收标准。当这些子场景未通过 system prompt 显式提供时，模型倾向于回退至满足结构与术语合规标准（自动评分与 LLM 评审最易捕获的维度，§3.6）但缺乏专家所识别的操作深度的通用程序化语言，而后者正是认可级文档的合规门槛。因此，prompt 精简化适用于以 LLM 单评为终审的快速草拟场景；当目标是经专家验证的合规性时，则需采用模板锚定的 prompt。

### 4.2 全量上下文陷阱的模型依赖性

虽然模板锚定可提升专家合规评分（§4.1），但当模型缺乏可靠的长上下文处理能力时，最大化扩展 prompt 反而可能适得其反。C_full（~56,000 tokens）代表一种直觉上的"安全"配置：包含全部潜在相关材料，符合"上下文越多越可靠"的常见启发式。然而本研究数据表明，这一启发式在两个生成模型之间并未一致成立。Claude Opus 4.6 在 C_full 下的跨评均值为 3.22–4.56 分（0–5 Likert 量纲；§3.3），而 GPT-5.4 在同一配置下仅得 1.40–1.84 分（基于 9 份文件——3 个代表性任务 × 3 次重复），并伴随 §3.3 记录的三种失败模式——指令遵循衰退、结构错乱、条款引用混淆。一个可能的解释（与 Liu 等 [3] 描述的 lost-in-the-middle 现象、以及两个模型族的厂商技术文档报告的长上下文 benchmark [1, 2] 一致）是：Claude Opus 4.6 在相关长度区间下维持了更稳定的注意力分配，而 GPT-5.4 在本研究测试的参数下未能在此规模下保持对 system prompt 约束的连贯遵从。

该研究的方法学含义是：形如"配置 X 可用"的任何论断都需要跨多个生成模型验证。单模型评估将配置效应与模型固有特性——包括长上下文处理能力、指令遵循稳定性、以及模型训练分布与目标监管领域的重合度——纠缠在一起，因而无法为跨模型外推提供依据。鉴于此，我们建议在任何 LLM 上部署长上下文 QMS prompt（例如接近或超过 ~50,000 tokens 的 prompt）前，必须在该具体模型与版本下完成验证；尤其因为长上下文行为可能在模型族之间、甚至在同一模型族的连续版本之间出现实质性变化。

### 4.3 评审员偏差概貌与 LLM-as-judge 的恰当使用

本研究量化了两种性质不同的评分偏差。第一种是跨判官方向性模式：两位 LLM 评审在 0–5 Likert 量纲下均把 Claude 生成输出评得比 GPT 生成高约 0.30 分（Panickssery 经典估计：Claude 评审 +0.29，GPT 评审 −0.30；§3.4）。然而如 §3.4 所述，该总体均值受 C_full 配置强力杠杆影响：排除 C_full 后，Claude 评审均值偏差衰减至 −0.064，GPT 评审均值偏差衰减至 −0.167，表明跨判官方向性模式集中于长上下文配置，而非 LLM-as-judge 框架的均匀属性。该符号相反的模式与"同家族经典自偏好"不兼容——后者应表现为两位判官均为同号正值——故可由 Claude Opus 4.6 与 GPT-5.4 之间真实的生成质量差异、或两位 LLM 评审共享的、偏向 Claude 生成文风的判官端偏好来解释。如 §4.2 与 §4.5(i) 所述，本研究设计——专家评分仅覆盖 Claude 生成文件——无法在两种解释之间充分判别；然 §3.3 记录的 GPT 特异性失败模式（指令遵循衰退、结构错乱、条款引用混淆）为存在真实生成质量贡献提供了间接支持。第二种是系统性的 LLM–专家偏移：两位 LLM 评审在同一量纲下均把专家判定的合规分数高估 0.52–0.90 分（§3.5）。

将上述偏差转化为实操指引：Claude 评审与三位专家均值排序的中等一致性 [ICC(3,1)=0.548，p=0.04] 使其可作为大规模生成管线中的粗筛代理，在专家审阅前先过滤明显低质量的输出；GPT 评审与专家一致性较差 [ICC(3,1)=0.217，p=0.26]，不宜作为专家评分的代理。对于拟提交认可、纳入正式 QMS 体系或投入实际操作的文件，专家终审仍属必需。这些偏差在配置层面的实操含义概括于 §4.4（Table 2）。

### 4.4 按使用场景分层的配置推荐

综合三层评估的证据，我们将面向 QMS 生成主要使用场景的配置推荐汇总于 Table 2。这些推荐反映了 §3.5 与 §3.6 所识别的核心权衡：在 LLM 评审层评分最高的配置（H4_sop_only、E_rules_v2）token 效率最佳，但缺乏认可级文档所需的临床实操深度；而模板锚定的配置（F_template、G_template_rules）在 LLM 评审层得分较低，却获得最高的专家合规评分。

**Table 2.** 按使用场景分层的配置推荐。

| 使用场景 | 推荐配置 | Tokens | 依据 | 权衡 |
|---|---|---|---|---|
| 快速生成首稿；内部迭代 | H4_sop_only 或 E_rules_v2 | ~1,000–2,000 | LLM 评审层近最优；token 效率最高 | 需人工补充临床细节 |
| 多 SOP 批量起草 | H4_sop_only 或 H3_skeleton | ~2,000–5,000 | 任务特定骨架 + 规则 | 需人工补充临床细节 |
| 正式 CNAS 送审文件 | G_template_rules | ~16,000 | 专家合规评分最高；跨模型稳健 | 较高 token 成本 |
| 完整质量手册 | F_template 或 G_template_rules | ~15,000–16,000 | 专家评分最高 | 较高 token 成本 |
| 不推荐 | C_full | ~56,000 | GPT-5.4 生成下崩溃；去偏后跨评排名最低 | — |
| 不推荐 | A_bare、B_simple | 0–~300 | prompt 锚定不足；低于实际合规基线 | — |

由本研究数据归纳的端到端实践工作流为：(i) 用 H4_sop_only 生成快速首稿；(ii) 通过人工评审或针对性再 prompt 补充临床实操细节；(iii) 用 G_template_rules 重生成或精修最终的认可级文档。

### 4.5 局限性

本研究存在以下局限。

**(i) 专家样本规模有限，且全部为 Claude 生成。** 专家层包含 3 位评分员对 10 份文件的评分（每层 n=1 或 2；见 §3.5），10 份样本全部抽取自 Claude 生成池；未对任何 GPT 生成文件开展专家评估。该设计仅支持 Claude 生成下的方向性排序结论，不允许严格统计推断；因此 §3.4 中 (a) Claude Opus 4.6 与 GPT-5.4 之间真实生成质量差异 与 (b) 两位判官共享的判官端风格偏好 之间的歧义，无法在本研究样本内判别。此外，§3.4 报告的跨判官偏差估计受 C_full 配置强力杠杆影响（C_full 贡献了 Claude 评审均值的最大单组值 +3.156 与 GPT 评审均值的最大负值 −1.378）；后续重复研究应分别报告各配置的偏差分布，以区分长上下文特异性效应与配置无关的判官偏好。所抽样的 10 份文件全部为 A 类程序文件（§2.3.3）；推广至 B 类（体系运行）与 C 类（审核模拟）任务需另行验证。跨单位 3 至 5 位评分员 × 30 至 50 份文件 / 单位（且包含匹配的 GPT 生成样本与 B/C 类任务）的多中心验证，是关键的未来工作。

**(ii) 同单位专家一致性可能高估可推广性。** 3 位专家间的极高一致性 [ICC(2,k)=0.982] 既支持 5 维度量规的有效性，也可能反映同一单位内共享的专业文化、培训谱系与对模糊条款的解读习惯。所观察到的可靠性可能因此高估跨单位一致性。

**(iii) 第一作者的双重角色。** 第一作者同时担任 Rater 1 与研究设计者。为减弱自我影响，Rater 2 与 Rater 3 在不知晓 Rater 1 评分的前提下独立完成评分；各 rater 数据完整公开供独立审核。

**(iv) 专家与 LLM 评审共享 5 维度量规。** 5 维度量规由 LLM 评审与专家评审同等使用，存在 shared-measurement bias 风险。未来工作应纳入专家原生维度——如部门工作流约束下的实操可实施性——这类维度难以从训练数据中由 LLM 内化获得。

**(v) GPT-5.4 任务覆盖受限。** 仅 A1、B1、C1 三个任务由 GPT-5.4 生成（81 份文件），跨模型结论限于这一三任务子集。

**(vi) 领域特异性。** 本研究结论限于 ISO 15189 医学实验室 QMS 文件；对相邻监管框架（例如检验与校准实验室的 ISO 17025、通用质量管理的 ISO 9001）的可迁移性需另行验证。

**(vii) LLM 评审范围受限。** 仅 Claude Opus 4.6 与 GPT-5.4 担任评审；所观察到的跨判官方向性偏差与专家高估模式是否可推广至其它模型家族（如 Gemini、开源权重模型），尚未知。

**(viii) 单语言范围。** 全部 QMS 文件以中文生成与评估；英文及其它语言下的配置效应与偏差概貌尚未验证。

**(ix) 模型时效性。** 本研究结论基于 2026 年 4 月 2 日至 14 日期间测试的具体模型版本与参数；随着 LLM 持续迭代，可能需要周期性重新验证。

**(x) 跨判官 cell 的 raw 数据保留不对称。** Claude 评审 × GPT 生成象限及 Claude 评审 × H 组 × Claude 生成子集的 per-document raw 评分仅以聚合均值形式归档，per-document JSON 文件未保留。完整的 2 × 2 自评偏差矩阵因此无法在 per-document 层面独立复算；不过 6 个核心配置（A/B/C/E/F/G；270 条评分）的 per-document Claude 评审 raw 数据与全部 486 条 GPT 评审 per-document 数据完整公开。

**(xi) 评审员内部一致性未评估。** 每位 LLM 评审员对每份文件仅打分一次，未要求评审员重复打分以量化内部方差。评审员间一致性通过 Claude 与 GPT 评审的 2 × 2 跨比较及 3 位专家 ICC 分析间接获得。

**(xii) 未开展评分前专家校准会议。** 3 位评分员仅依据公布的量规与 ISO 15189:2022 / CNAS-CL02:2023 标准独立评分，未事先开展校准会议（即由 3 位评分员先共同评分若干示例文件以对齐解读）。极高的评审员间一致性表明该量规在本单位语境下已足够自解释，但在多中心研究中加入正式校准步骤将有助于增强可重复性。

**(xiii) Claude Code Agent 封装。** Claude Opus 4.6 的生成与 Claude 评审通过 Claude Code Agent 工具执行，而非直接 Anthropic SDK 调用。Claude Code 框架在每条 user-supplied prompt 之上叠加恒定的 framework 级 system prompt（工具定义与文件系统指引）；故模型实际接收的 prompt 长度大于 §2.1 报告的 per-config token 数。该 framework 开销在所有 9 配置与所有评审调用中保持一致，故配置间相对比较与判官-专家一致性结论不受影响；但要精确复现绝对评分需使用相同 Claude Code 版本。以直接 Anthropic SDK 调用相同配置可能得到略有差异的绝对评分。

**(xiv) AIHubMix 路由未独立审计。** GPT-5.4 通过 AIHubMix 代理调用，该代理宣称对上游 OpenAI API 透明转发。本研究未独立验证其响应与直接 OpenAI 调用的等价性；路由层面的细微差异（请求批处理、header 处理、地域路由）无法完全排除，但 GPT-5.4 model 标识符在调用链路中保持一致。

**(xv) 温度设置。** 所有生成均使用 temperature = 1.0 以反映真实交互使用场景。此设置引入随机性方差（已通过每元胞 3 次重复缓解），但牺牲了严格的字面级可重复性；追求确定性比较的后续研究建议改用 temperature = 0。

---

## 5. Conclusions

LLM 辅助 ISO 15189 QMS 文件生成的最优 prompt 配置取决于评估层。在 LLM 评审层，H4_sop_only（~2,000 tokens）综合分最高；然而在专家评估下，专家评分前三的配置为模板锚定的 F_template（~15,000 tokens）、H2_keep_examples（~25,000 tokens）与 G_template_rules（~16,000 tokens）（均值 = 4.06–4.24 分，0–5 Likert 量纲），而 H4_sop_only 跌至 7 配置中的第 5 名，仅高于空 prompt 基线 A_bare 0.16 分。因此，极简 prompt 配置（H4_sop_only 或 E_rules_v2；~1,000–2,000 tokens）适合用于将经后续专家审阅的探索性草稿；而模板锚定配置（G_template_rules 或 F_template；~15,000–16,000 tokens）对于拟提交 CNAS 或同等 ISO 15189 认可的文件则属必需。C_full（~56,000 tokens）在本研究情境下应避免使用，尤其是在生成模型为 GPT-5.4 时——参见 §3.3 记录的长上下文失败模式。LLM-as-judge 方法可作为首道筛选工具：Claude 评审与专家排序的中等一致性 [ICC(3,1) = 0.548] 使其可作为审慎的代理；GPT-5.4 评审 [ICC(3,1) = 0.217] 不适合此用途。对于拟提交认可、纳入正式 QMS 体系或投入实际操作的任何文件，专家终审仍属必需。

据我们所知，本研究是首个跨两个前沿 LLM 与三层次评估框架对 ISO 15189 合规 QMS 文件生成中 prompt 内容效应进行系统性比较的研究；研究发现为实验室认可工作流中的 prompt 设计指南提供了实证基础。

---

## 申报声明

**Research funding**：本研究未接受外部研究资助。

**Author contributions**：刘斯迪独立承担本研究的概念与设计、全部实验的执行、数据分析、稿件的撰写与定稿，并对文章内容承担全部责任。

**Competing interests**：作者声明不存在任何利益冲突。

**Informed consent**：在 Rater 2 与 Rater 3 参与盲法专家评审前已获得书面知情同意。同意书载明了研究目的、评分的预期用途、数据处理与去标识化程序，以及随时退出的权利。

**Ethical approval**：本研究不需要正式的伦理审批，因不涉及患者数据、生物样本或人体干预。所生成与所评估的 QMS 文件使用虚构占位姓名（如"Dr Li"、"Dr Zhang"）且不含任何可识别个人信息。评分员间数据集作为方法学研究自知情同意志愿者处采集；评分员层面的可识别数据在公开数据集中以编码标签（Rater 1 / Rater 2 / Rater 3）存储。

**Data availability**：486 份生成文件、864 条 LLM-as-judge 评分、30 条盲法专家评分以及全部分析代码已在 GitHub 公开（https://github.com/stttttte/iso15189-llm-config-experiment），采用双许可证：代码 MIT，数据 CC BY 4.0。版本化快照已在 Zenodo 归档（DOI：[接收后分配]）。

---

## 致谢

作者感谢两位参与盲法专家评审的同事（Rater 2 与 Rater 3），他们在充分知情同意的前提下提供了独立的专家视角。

---

## References

1. Anthropic. Claude Opus 4.6 System Card. 2025. Available at: https://www.anthropic.com/claude

2. OpenAI. GPT-5 System Card. 2025. Available at: https://openai.com/

3. Liu NF, Lin K, Hewitt J, Paranjape A, Bevilacqua M, Petroni F, et al. Lost in the middle: how language models use long contexts. Trans Assoc Comput Linguist 2024;12:157–73.

4. Zhao WX, Zhou K, Li J, Tang T, Wang X, Hou Y, et al. A survey of large language models. arXiv preprint 2023; arXiv:2303.18223.

5. Zheng L, Chiang WL, Sheng Y, Zhuang S, Wu Z, Zhuang Y, et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. In: Advances in Neural Information Processing Systems. 2023.

6. Panickssery A, Bowman SR, Feng S. LLM evaluators recognize and favor their own generations. arXiv preprint 2024; arXiv:2404.13076.

7. ISO 15189:2022. Medical laboratories — Requirements for quality and competence. Geneva: International Organization for Standardization; 2022.

8. Boiko DA, MacKnight R, Kline B, Gomes G. Autonomous chemical research with large language models. Nature 2023;624:570–8.

9. Jin D, Pan E, Oufattole N, Weng WH, Fang H, Szolovits P. What disease does this patient have? A large-scale open domain question answering dataset from medical exams. Appl Sci 2021;11:6421.

10. Tan H, Guo Z, Shi Z, Xu L, Liu Z, Li X, et al. ProxyQA: an alternative framework for evaluating long-form text generation with large language models. In: Proceedings of ACL. 2024.

11. Chiang WL, Zheng L, Sheng Y, Angelopoulos AN, Li T, Li D, et al. Chatbot Arena: an open platform for evaluating LLMs by human preference. arXiv preprint 2024; arXiv:2403.04132.

12. Schulhoff S, Ilie M, Balepur N, Kahadze K, Liu A, Si C, et al. The prompt report: a systematic survey of prompting techniques. arXiv preprint 2024; arXiv:2406.06608.

13. Shrout PE, Fleiss JL. Intraclass correlations: uses in assessing rater reliability. Psychol Bull 1979;86:420–8.

14. Yang S, Zhou Y, Wang C, Luo M. The 'Double Helix' model of quality monitoring: risk mapping of quality management system during initial ISO 15189 implementation in a medical laboratory. PLoS One 2026;21:e0342129.

15. Cicchetti DV. Guidelines, criteria, and rules of thumb for evaluating normed and standardized assessment instruments in psychology. Psychol Assess 1994;6:284–90.

---

**Word count (正文含参考文献)**：约 6200 字  
**Tables**：6（含推荐配置表 Table 2）  
**Figures**：4  
**References**：15
