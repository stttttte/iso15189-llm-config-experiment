#!/usr/bin/env python3
"""
三层混合评分脚本
================
第一层：自动化评分（格式18% + 条款22% + 术语13% = 53%）
第二层：LLM-as-Judge 评分（逻辑18% + 可操作性10% + 安全9% + 修改量10% = 47%）
第三层：人工校验（抽样 10%，计算相关性）

用法：
  python auto_scorer.py --phase auto     # 仅自动化评分
  python auto_scorer.py --phase llm      # LLM-as-Judge 评分
  python auto_scorer.py --phase merge    # 合并所有评分
  python auto_scorer.py --phase sample   # 抽取人工校验样本
"""

import os
import sys
import json
import re
import random
import argparse
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
SCORES_DIR = BASE_DIR / "scores"
LOGS_DIR = BASE_DIR / "logs"

# 七维度权重
WEIGHTS = {
    "格式": 0.18,
    "条款": 0.22,
    "术语": 0.13,
    "逻辑": 0.18,
    "可操作性": 0.10,
    "安全合规性": 0.09,
    "人工修改量": 0.10,
}

# ==================== 第一层：自动化评分 ====================

# ---- 分类格式标准 ----

# A 类（程序文件）：八段结构（接受同义变体）
FORMAT_STANDARDS_A = {
    "name": "程序文件八段结构",
    "required_sections": ["目的", "适用范围", "职责", "定义", "程序内容", "相关文件", "记录表格", "变更历史"],
    "alt_sections":      ["目的", "适用范围", "职责", "术语", "程序内容", "相关文件", "记录表单", "修订历史"],
    "total": 8,
}

# B 类（体系运行）：检查表/报告类格式
FORMAT_STANDARDS_B = {
    "name": "检查表/报告格式",
    "required_sections": ["标题", "编号", "日期", "检查项目", "结果", "结论"],
    "alt_sections": ["表头", "编号", "日期", "数据", "判定", "签名"],  # 备选匹配
    "total": 6,
}

# C 类（审核模拟）：审查报告格式
FORMAT_STANDARDS_C = {
    "name": "审查报告格式",
    "required_sections": ["审查目的", "审查范围", "审查依据", "发现", "不符合项", "建议", "结论"],
    "alt_sections": ["目的", "范围", "依据", "审查发现", "不符合", "整改建议", "总结"],
    "total": 7,
}

# 保持向后兼容
EIGHT_SECTIONS = FORMAT_STANDARDS_A["required_sections"]

# 术语对照表（旧术语 → 标准术语）
# 经领域专家（检验科人员）校验，基于 ISO 15189:2022 / CNAS-CL02:2023
TERMINOLOGY_MAP = {
    "分析前过程": "检验前过程",
    "分析前阶段": "检验前过程",
    "分析过程": "检验过程",
    "分析阶段": "检验过程",
    "分析后过程": "检验后过程",
    "分析后阶段": "检验后过程",
    "不确定度": "测量不确定度",  # 单独的"不确定度"算旧术语
    "正常值范围": "生物参考区间",
    "正常参考值": "生物参考区间",
    "正常值": "生物参考区间",
    "参考值": "生物参考区间",
    "标本": "样品",      # 标准术语为"样品"（非"样本"）
    "检验项目": "检测项目",  # "检验项目"应为"检测项目"；注意"检验程序"是另一概念
    "准确度": "正确度",
    "质控品": "质控物",
    "线性范围": "可报告范围",  # 非"测量区间"
    # 以下已删除（经专家校验不成立）：
    # "仪器" → "设备"：仪器在特定语境下合理，不需强制替换
    # "校准品" → "校准物"：校准品本身就是标准术语
    # "室间质评" → "能力验证"：两者是不同概念，不应互相替代
}

# 歧义术语的上下文排除规则
# 当旧术语出现在这些模式中时，不计为违规
# 注意："仪器"已从术语表中删除（特定语境下合理），无需排除规则
CONTEXT_EXCEPTIONS = {
    "不确定度": [
        r"测量不确定度",
        r"扩展不确定度",
        r"合成不确定度",
        r"合成标准不确定度",
        r"不确定度评定",
        r"不确定度估算",
    ],
    "检验项目": [
        r"检验项目/检测项目",   # 同时使用了两个术语的过渡写法
        r"检验项目（检测项目）",
    ],
}


def _count_term_violations(old_term: str, text: str) -> list[tuple[int, str]]:
    """
    返回旧术语在文本中的所有违规位置。
    对有上下文排除规则的术语，先排除合理用法再计数。
    返回: [(match_start, context_snippet), ...]
    """
    exceptions = CONTEXT_EXCEPTIONS.get(old_term, [])

    # 先找出所有排除模式的匹配区间
    excluded_ranges = set()
    for exc_pattern in exceptions:
        for m in re.finditer(re.escape(exc_pattern), text):
            for pos in range(m.start(), m.end()):
                excluded_ranges.add(pos)

    # 特殊处理：不确定度的原始 lookbehind 逻辑也保留
    if old_term == "不确定度":
        pattern = re.compile(r"不确定度")
    else:
        pattern = re.compile(re.escape(old_term))

    violations = []
    for m in pattern.finditer(text):
        # 如果匹配位置在排除区间内，跳过
        if m.start() in excluded_ranges:
            continue
        # 提取上下文片段（前后各 20 字符）
        start = max(0, m.start() - 20)
        end = min(len(text), m.end() + 20)
        context = text[start:end].replace("\n", " ")
        violations.append((m.start(), context))

    return violations


# 模糊表述黑名单
VAGUE_PATTERNS = [
    r"大约|约\d|左右|差不多",
    r"一般来说|通常|往往",
    r"及时|尽快|尽早",
    r"相关人员|有关部门",
    r"适当|合理(?!性)|必要时",
    r"定期(?!审)|经常|不定期",
    r"做好记录|注意保存",
]

# B 部分：复合词白名单（在表头/分类/定义语境中不计为模糊）
VAGUE_COMPOUND_EXCEPTIONS = {
    "定期": [
        r"定期评估",        # 评估类型名称（"初始/定期/触发"分类）
        r"定期能力评估",
        r"定期考核",
        r"定期重新评估",    # ISO 条款原文引用
    ],
    "适当": [
        r"适当组合",        # ISO 术语定义引用（"教育、培训和经验的适当组合"）
    ],
}

# A 部分：频率类量化词（用于上下文窗口检测）
# 只匹配频率/时限类量化，不匹配分数/百分比/保存期限等非频率数值
FREQUENCY_QUANTIFIER = re.compile(
    r'每\s*(月|周|年|季度|半年|日|天|批次|班次)'
    r'|\d+\s*(个月|天|日|小时|次/|周|工作日)内?'
    r'|每\s*\d+\s*(个月|天|日|小时|周)'
    r'|[年月周日]\s*[1-9一二三四]\s*次'
)


def _count_vague_violations(text: str) -> list[tuple[str, str]]:
    """
    检测模糊表述，返回真正的违规列表。
    对每个匹配应用双重过滤：
    1. 复合词白名单（B）：命中则跳过
    2. 上下文量化检测（A）：后续30字符内有频率类量化则跳过
    返回: [(匹配词, 上下文片段), ...]
    """
    violations = []

    for pattern in VAGUE_PATTERNS:
        for m in re.finditer(pattern, text):
            matched_word = m.group()

            # B 部分：检查复合词白名单
            exceptions = VAGUE_COMPOUND_EXCEPTIONS.get(matched_word, [])
            is_compound = False
            for exc in exceptions:
                # 检查匹配位置是否在复合词内
                exc_start = max(0, m.start() - 5)
                exc_end = min(len(text), m.end() + 20)
                window = text[exc_start:exc_end]
                if re.search(exc, window):
                    is_compound = True
                    break
            if is_compound:
                continue

            # A 部分：检查后续30字符内是否有频率类量化
            after_text = text[m.end():m.end() + 30]
            if FREQUENCY_QUANTIFIER.search(after_text):
                continue

            # 通过双重过滤，计为真正的模糊违规
            start = max(0, m.start() - 20)
            end = min(len(text), m.end() + 20)
            context = text[start:end].replace("\n", " ")
            violations.append((matched_word, context))

    return violations

# ISO 15189:2022 有效条款号范围（第4-8章）
VALID_CLAUSE_PREFIXES = ["4.", "5.", "6.", "7.", "8."]


def _detect_task_category(filename: str) -> str:
    """从文件名推断任务类别：A/B/C"""
    # 文件名格式: {group}-{taskId}-{repeat}.md, e.g. C_full-A3-2
    parts = filename.replace(".md", "").split("-")
    for p in parts:
        if p and p[0] in ("A", "B", "C") and len(p) <= 3:
            # 可能是 task_id 如 A1, B3, C5；也可能是组名如 A_bare
            if p[0] in ("A", "B", "C") and len(p) == 2 and p[1].isdigit():
                return p[0]
    # fallback: 默认 A 类
    return "A"


def score_format(text: str, task_category: str = "A") -> tuple[int, dict]:
    """自动评分：格式维度（1-5分），按任务类别使用不同标准"""
    details = {}
    score = 5

    # 选择对应类别的格式标准
    if task_category == "B":
        standard = FORMAT_STANDARDS_B
    elif task_category == "C":
        standard = FORMAT_STANDARDS_C
    else:
        standard = FORMAT_STANDARDS_A

    details["评分标准"] = standard["name"]

    # 检查必要章节（主列表 + 备选列表合并匹配）
    required = standard["required_sections"]
    alt = standard.get("alt_sections", [])

    found_sections = []
    for i, section in enumerate(required):
        if section in text:
            found_sections.append(section)
        elif i < len(alt) and alt[i] in text:
            found_sections.append(alt[i])

    n_required = standard["total"]
    found_count = len(found_sections)
    details["结构匹配"] = f"{found_count}/{n_required}: {found_sections}"
    missing = n_required - found_count

    if missing >= 3:
        score = 1
    elif missing == 2:
        score = 2
    elif missing == 1:
        score = 3
    else:
        score = 5

    # 检查编号层级
    numbering_pattern = re.findall(r"(?m)^#{1,4}\s*\d+(?:\.\d+)*", text)
    if not numbering_pattern:
        numbering_pattern = re.findall(r"(?m)^\d+(?:\.\d+)*\s", text)
    details["编号层级数"] = len(numbering_pattern)
    if len(numbering_pattern) < 3:
        score = min(score, 3)

    # 检查是否有空章节（仅检测同级或更高级标题紧接的情况，排除父标题→子标题的正常嵌套）
    empty_count = 0
    heading_pattern = re.compile(r"^(#{1,6})\s+.+", re.MULTILINE)
    headings = list(heading_pattern.finditer(text))
    for i in range(len(headings) - 1):
        curr_level = len(headings[i].group(1))
        next_level = len(headings[i + 1].group(1))
        # 只有下一个标题层级 <= 当前标题（同级或更高），中间无实质内容，才算空章节
        if next_level <= curr_level:
            between = text[headings[i].end():headings[i + 1].start()].strip()
            if not between:
                empty_count += 1
    details["疑似空章节"] = empty_count
    if empty_count > 2:
        score = min(score, 3)

    return score, details


def score_clause(text: str) -> tuple[int, dict]:
    """自动评分：条款覆盖维度（1-5分）"""
    details = {}

    # 提取所有疑似条款号，并用上下文关键词过滤误匹配
    CLAUSE_CONTEXT_KEYWORDS = re.compile(
        r"ISO|CNAS|条款|条|标准|要求|规定|依据|参照|参见|见|符合|按照|根据|15189|CL02|GB"
    )
    raw_matches = list(re.finditer(
        r"(?:ISO\s*15189(?::2022)?\s*)?(?:第\s*)?(\d+\.\d+(?:\.\d+)?)\s*(?:条)?", text
    ))

    valid_clauses = []
    for m in raw_matches:
        clause_num = m.group(1)
        if not any(clause_num.startswith(p) for p in VALID_CLAUSE_PREFIXES):
            continue
        # 检查前后 40 字符的上下文窗口是否包含条款相关关键词
        start = max(0, m.start() - 40)
        end = min(len(text), m.end() + 40)
        context_window = text[start:end]
        if CLAUSE_CONTEXT_KEYWORDS.search(context_window):
            valid_clauses.append(clause_num)
        # 如果匹配串本身含有 "ISO" 前缀也算（已在 regex 中捕获）
        elif "ISO" in m.group(0) or "第" in m.group(0):
            valid_clauses.append(clause_num)

    unique_clauses = sorted(set(valid_clauses))

    details["引用条款数"] = len(unique_clauses)
    details["条款列表"] = unique_clauses[:20]  # 截断避免过长

    # 检查 CNAS-CL02 引用
    cnas_refs = re.findall(r"CNAS[-\s]*CL02", text)
    details["CNAS引用次数"] = len(cnas_refs)

    # 评分逻辑
    n_clauses = len(unique_clauses)
    has_cnas = len(cnas_refs) > 0

    if n_clauses == 0:
        score = 1
    elif n_clauses <= 2:
        score = 2
    elif n_clauses <= 5:
        score = 3
    elif n_clauses <= 10:
        score = 4
    else:
        score = 5

    # CNAS 引用加分/减分
    if not has_cnas and score >= 3:
        score -= 1
        details["扣分原因"] = "缺少 CNAS-CL02 引用"

    return score, details


def score_terminology(text: str) -> tuple[int, dict]:
    """自动评分：术语维度（1-5分），支持上下文排除"""
    details = {}
    violations = []

    for old_term, new_term in TERMINOLOGY_MAP.items():
        term_violations = _count_term_violations(old_term, text)
        count = len(term_violations)
        if count > 0:
            violations.append({"旧术语": old_term, "应为": new_term, "出现次数": count})

    details["术语违规"] = violations
    details["违规总数"] = sum(v["出现次数"] for v in violations)

    # 检查模糊表述（使用上下文过滤 + 复合词白名单）
    vague_violations = _count_vague_violations(text)
    vague_count = len(vague_violations)
    vague_matches = [v[0] for v in vague_violations[:10]]  # 最多记录10个
    details["模糊表述"] = vague_matches
    details["模糊表述数"] = vague_count

    # 评分
    total_issues = details["违规总数"] + vague_count
    if total_issues >= 5:
        score = 1
    elif total_issues >= 3:
        score = 2
    elif total_issues >= 1:
        score = 3
    elif total_issues == 0 and vague_count == 0:
        score = 5
    else:
        score = 4

    return score, details


def auto_score_file(filepath: Path) -> dict:
    """对单个文件执行三维度自动化评分"""
    text = filepath.read_text(encoding="utf-8")

    task_category = _detect_task_category(filepath.name)
    fmt_score, fmt_details = score_format(text, task_category=task_category)
    cls_score, cls_details = score_clause(text)
    trm_score, trm_details = score_terminology(text)

    return {
        "file": str(filepath.name),
        "scores": {
            "格式": fmt_score,
            "条款": cls_score,
            "术语": trm_score,
        },
        "details": {
            "格式": fmt_details,
            "条款": cls_details,
            "术语": trm_details,
        },
        "text_length": len(text),
        "scored_at": datetime.now().isoformat(),
    }


# ==================== 第二层：LLM-as-Judge ====================

LLM_JUDGE_PROMPT = """你是一名 ISO 15189:2022 质量管理体系文件评审专家。请对以下文件进行专业评分。

## 评分维度与标准

请对以下 4 个维度分别打 1-5 分：

### 1. 逻辑（权重 18%）
- 1分：存在明显矛盾或逻辑缺环（如前后步骤矛盾、流程未闭环）
- 2分：逻辑链不完整，有2处以上逻辑跳跃
- 3分：逻辑基本通顺，但有1-2处衔接不紧密
- 4分：逻辑清晰，流程闭环完整，仅有细微可改进处
- 5分：逻辑严密，因果关系清晰，PDCA闭环完整

### 2. 可操作性（权重 10%）
- 1分：步骤笼统模糊，无法直接执行
- 2分：部分步骤可执行，但多数需要额外细化
- 3分：基本可执行，但有2-3个步骤需要补充细节
- 4分：绝大部分步骤可直接执行，仅1处需细化
- 5分：每个步骤均可直接执行，含明确的人、时、方法、标准

### 3. 安全合规性（权重 9%）
- 1分：完全缺失安全和保密相关内容
- 2分：仅提及"注意安全"等笼统表述
- 3分：包含部分安全要求但不全面
- 4分：安全要求较全面，涵盖人员防护和数据安全
- 5分：全面覆盖生物安全、个人防护、数据安全、患者隐私等

### 4. 人工修改量（权重 10%）
- 1分：需重写 > 50%，基本不可用
- 2分：需重写 30-50%
- 3分：需修改 20-30%，框架可用但细节需调整
- 4分：需修改 10-20%，主要是微调
- 5分：需修改 < 10%，几乎可直接使用

## 输出格式

请严格按以下 JSON 格式输出，不要输出其他内容：

```json
{
  "逻辑": {"score": <1-5>, "reason": "<简述理由>"},
  "可操作性": {"score": <1-5>, "reason": "<简述理由>"},
  "安全合规性": {"score": <1-5>, "reason": "<简述理由>"},
  "人工修改量": {"score": <1-5>, "reason": "<简述理由>"}
}
```

## 待评分文件

"""


LLM_JUDGE_ROUNDS = 3  # 每份文件评分次数，取中位数


def _single_llm_call(prompt: str) -> dict | None:
    """单次 LLM Judge 调用，返回解析后的评分 dict 或 None（通过 AIHubMix 代理）"""
    try:
        from openai import OpenAI
        api_key = os.environ.get("GPT_API_KEY", "")
        base_url = os.environ.get("OPENAI_BASE_URL", "https://aihubmix.com/v1")
        if not api_key:
            print("  [ERROR] 请设置环境变量 GPT_API_KEY")
            return None
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model="gpt-5.4",
            temperature=0.3,  # 略高温度配合多次调用，增加评分多样性以衡量稳定性
            max_completion_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        raw_output = response.choices[0].message.content
    except Exception as e:
        print(f"  [ERROR] LLM Judge 调用失败: {e}")
        return None

    try:
        json_match = re.search(r"\{[\s\S]*\}", raw_output)
        if json_match:
            scores = json.loads(json_match.group())
        else:
            scores = json.loads(raw_output)
        return scores
    except json.JSONDecodeError:
        print(f"  [WARNING] JSON 解析失败，原始输出: {raw_output[:200]}")
        return None


def llm_judge_score(filepath: Path, n_rounds: int = LLM_JUDGE_ROUNDS) -> dict:
    """使用 GPT-5.4 作为评审员对文件进行主观维度评分（多次调用取中位数）"""
    import statistics
    import time as _time

    text = filepath.read_text(encoding="utf-8")

    # 截断过长的文件（避免token溢出）
    if len(text) > 12000:
        text = text[:12000] + "\n\n[文件过长，已截断至前12000字]"

    prompt = LLM_JUDGE_PROMPT + text

    # 多轮调用
    all_round_scores = []  # list of dicts
    all_round_reasons = []
    dims = ["逻辑", "可操作性", "安全合规性", "人工修改量"]

    for rd in range(n_rounds):
        parsed = _single_llm_call(prompt)
        if parsed is None:
            continue
        round_scores = {dim: parsed[dim]["score"] for dim in dims if dim in parsed}
        round_reasons = {dim: parsed[dim]["reason"] for dim in dims if dim in parsed}
        all_round_scores.append(round_scores)
        all_round_reasons.append(round_reasons)
        if rd < n_rounds - 1:
            _time.sleep(0.5)

    if not all_round_scores:
        return {"error": "所有轮次调用均失败"}

    # 取中位数作为最终评分
    final_scores = {}
    score_variance = {}
    for dim in dims:
        dim_values = [rs[dim] for rs in all_round_scores if dim in rs]
        if dim_values:
            final_scores[dim] = int(statistics.median(dim_values))
            score_variance[dim] = round(statistics.variance(dim_values), 4) if len(dim_values) > 1 else 0.0
        else:
            final_scores[dim] = 3  # fallback
            score_variance[dim] = None

    # 取中位数轮次对应的 reason（选距中位数最近的一轮）
    final_reasons = all_round_reasons[0] if all_round_reasons else {}
    if len(all_round_scores) > 1:
        # 选择加权总分最接近中位数的那轮的 reason
        median_total = sum(final_scores.values())
        diffs = [abs(sum(rs.get(d, 3) for d in dims) - median_total) for rs in all_round_scores]
        best_idx = diffs.index(min(diffs))
        final_reasons = all_round_reasons[best_idx] if best_idx < len(all_round_reasons) else final_reasons

    return {
        "file": str(filepath.name),
        "scores": final_scores,
        "reasons": final_reasons,
        "scored_at": datetime.now().isoformat(),
        "judge_model": "gpt-5.4",
        "n_rounds": len(all_round_scores),
        "all_round_scores": all_round_scores,
        "score_variance": score_variance,  # 各维度评分方差（内部一致性指标）
    }


# ==================== 合并与汇总 ====================

def merge_scores():
    """合并自动评分和 LLM 评分，计算加权综合得分"""
    auto_dir = SCORES_DIR / "auto"
    llm_dir = SCORES_DIR / "llm"
    merged_dir = SCORES_DIR / "merged"
    merged_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    for auto_file in sorted(auto_dir.glob("*.json")):
        filename = auto_file.stem
        with open(auto_file) as f:
            auto_data = json.load(f)

        llm_file = llm_dir / f"{filename}.json"
        if llm_file.exists():
            with open(llm_file) as f:
                llm_data = json.load(f)
        else:
            llm_data = {"scores": {"逻辑": 3, "可操作性": 3, "安全合规性": 3, "人工修改量": 3}}
            print(f"  [WARNING] 缺少 LLM 评分: {filename}，使用默认 3 分")

        # 合并七维度得分
        all_scores = {}
        all_scores.update(auto_data.get("scores", {}))
        all_scores.update(llm_data.get("scores", {}))

        # 计算加权综合得分
        weighted_sum = sum(all_scores.get(dim, 3) * w for dim, w in WEIGHTS.items())

        result = {
            "file": filename,
            "scores_by_dimension": all_scores,
            "weighted_total": round(weighted_sum, 3),
            "auto_details": auto_data.get("details", {}),
            "llm_reasons": llm_data.get("reasons", {}),
        }
        all_results.append(result)

        # 保存单文件合并结果
        with open(merged_dir / f"{filename}.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    # 保存汇总表
    summary_file = SCORES_DIR / "score_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"合并完成: {len(all_results)} 份文件")
    print(f"汇总文件: {summary_file}")

    # 输出 CSV 方便分析
    csv_file = SCORES_DIR / "score_summary.csv"
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write("file,格式,条款,术语,逻辑,可操作性,安全合规性,人工修改量,加权总分\n")
        for r in all_results:
            s = r["scores_by_dimension"]
            f.write(f"{r['file']},{s.get('格式',0)},{s.get('条款',0)},{s.get('术语',0)},{s.get('逻辑',0)},{s.get('可操作性',0)},{s.get('安全合规性',0)},{s.get('人工修改量',0)},{r['weighted_total']}\n")
    print(f"CSV 文件: {csv_file}")


def sample_for_human_validation(n=50, stratify=True):
    """抽取人工校验样本（支持按组别分层等比例抽样）"""
    merged_dir = SCORES_DIR / "merged"
    if not merged_dir.exists():
        print("请先运行 --phase merge")
        return

    all_files = sorted(merged_dir.glob("*.json"))

    if stratify:
        # 按组别分层等比例抽样
        group_files = {}
        for f in all_files:
            group_key = f.stem.split("-")[0]  # e.g. A_bare, B_simple, C_full, D_D1...
            group_files.setdefault(group_key, []).append(f)

        sample = []
        total_count = len(all_files)
        remaining = n
        groups_sorted = sorted(group_files.keys())

        for i, gk in enumerate(groups_sorted):
            gf = group_files[gk]
            if i == len(groups_sorted) - 1:
                # 最后一组分配剩余名额，避免舍入误差
                alloc = remaining
            else:
                alloc = max(1, round(n * len(gf) / total_count))
                remaining -= alloc
            actual = min(alloc, len(gf))
            sample.extend(random.sample(gf, actual))
            print(f"  分层抽样: {gk} → {actual}/{len(gf)}")

        sample_size = len(sample)
        print(f"  分层抽样总计: {sample_size} 份 (目标 {n})")
    else:
        sample_size = min(n, len(all_files))
        sample = random.sample(all_files, sample_size)

    sample_dir = SCORES_DIR / "human_validation_sample"
    sample_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for sf in sample:
        with open(sf) as f:
            data = json.load(f)

        # 找到对应的输出文件
        filename = data["file"]
        manifest.append({
            "编号": filename,
            "自动评分_格式": data["scores_by_dimension"].get("格式"),
            "自动评分_条款": data["scores_by_dimension"].get("条款"),
            "自动评分_术语": data["scores_by_dimension"].get("术语"),
            "LLM评分_逻辑": data["scores_by_dimension"].get("逻辑"),
            "LLM评分_可操作性": data["scores_by_dimension"].get("可操作性"),
            "LLM评分_安全合规性": data["scores_by_dimension"].get("安全合规性"),
            "LLM评分_人工修改量": data["scores_by_dimension"].get("人工修改量"),
            "人工评分_格式": "",
            "人工评分_条款": "",
            "人工评分_术语": "",
            "人工评分_逻辑": "",
            "人工评分_可操作性": "",
            "人工评分_安全合规性": "",
            "人工评分_人工修改量": "",
        })

    # 保存清单（不含自动评分结果，避免锚定效应）
    blind_manifest = []
    for m in manifest:
        blind_manifest.append({
            "编号": m["编号"],
            "人工评分_格式": "",
            "人工评分_条款": "",
            "人工评分_术语": "",
            "人工评分_逻辑": "",
            "人工评分_可操作性": "",
            "人工评分_安全合规性": "",
            "人工评分_人工修改量": "",
        })

    # 保存盲审清单（给人工评分员）
    with open(sample_dir / "blind_scoring_sheet.json", "w", encoding="utf-8") as f:
        json.dump(blind_manifest, f, ensure_ascii=False, indent=2)

    # 保存完整清单（用于后续相关性分析）
    with open(sample_dir / "full_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"已抽取 {sample_size} 份样本到 {sample_dir}")
    print(f"盲审评分表: blind_scoring_sheet.json（发给人工评分员）")
    print(f"完整对照表: full_manifest.json（评分完成后用于相关性分析）")


# ==================== 批量执行 ====================

def run_auto_scoring(phase="main"):
    """批量执行自动化评分"""
    output_dir = OUTPUTS_DIR / phase
    if not output_dir.exists():
        print(f"输出目录不存在: {output_dir}")
        return

    score_dir = SCORES_DIR / "auto"
    score_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(output_dir.rglob("*.md"))
    print(f"发现 {len(files)} 个待评分文件")

    for i, fp in enumerate(files):
        exp_id = fp.stem
        score_file = score_dir / f"{exp_id}.json"
        if score_file.exists():
            continue

        result = auto_score_file(fp)
        with open(score_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        if (i + 1) % 50 == 0:
            print(f"  进度: {i+1}/{len(files)}")

    print(f"自动化评分完成: {len(files)} 份")


def run_llm_scoring(phase="main"):
    """批量执行 LLM-as-Judge 评分"""
    output_dir = OUTPUTS_DIR / phase
    if not output_dir.exists():
        print(f"输出目录不存在: {output_dir}")
        return

    score_dir = SCORES_DIR / "llm"
    score_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(output_dir.rglob("*.md"))
    print(f"发现 {len(files)} 个待评分文件")

    import time
    for i, fp in enumerate(files):
        exp_id = fp.stem
        score_file = score_dir / f"{exp_id}.json"
        if score_file.exists():
            continue

        print(f"  [{i+1}/{len(files)}] LLM 评分: {exp_id}...", end=" ", flush=True)
        result = llm_judge_score(fp)
        with open(score_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("完成")
        time.sleep(0.5)

    print(f"LLM 评分完成: {len(files)} 份")


# ==================== 入口 ====================

def main():
    parser = argparse.ArgumentParser(description="三层混合评分脚本")
    parser.add_argument("--phase", choices=["auto", "llm", "merge", "sample", "all"],
                        default="auto", help="评分阶段")
    parser.add_argument("--experiment", default="main",
                        help="评分对象（main/ablation/external/supplement）")
    args = parser.parse_args()

    SCORES_DIR.mkdir(parents=True, exist_ok=True)

    if args.phase == "auto":
        run_auto_scoring(args.experiment)
    elif args.phase == "llm":
        run_llm_scoring(args.experiment)
    elif args.phase == "merge":
        merge_scores()
    elif args.phase == "sample":
        sample_for_human_validation()
    elif args.phase == "all":
        run_auto_scoring(args.experiment)
        run_llm_scoring(args.experiment)
        merge_scores()
        sample_for_human_validation()


if __name__ == "__main__":
    main()
