"""
H4 消融：每个任务只用最相关 SOP 骨架（而非整个模块）
- 测试：进一步精简到 SOP 级别，是否仍能保持质量？
- 预期大小：3-6K（比 H3 的 13K 再降 ~70%）
"""

import re

DOCS_DIR = "/Users/liusidi/Desktop/15189/15189-docs"
FIXES_DIR = "/Users/liusidi/Desktop/experiment_fixes"

# 任务 → (模块, [SOP 编号列表])
# SOP 编号对应模块内的 "# SOP N:" 标题
TASK_SOP_MAP = {
    "A1": ("04-程序文件-人员管理.md", [2, 3]),           # 能力评估+培训
    "A2": ("05-程序文件-设施设备试剂.md", [2]),           # 设备管理
    "A3": ("06-程序文件-检验流程.md", [1]),               # 检验前过程
    "A4": ("07-程序文件-质量保证与改进.md", [5]),         # 管理评审程序
    "A5": ("05-程序文件-设施设备试剂.md", [3]),           # 校准和计量溯源
    "B1": ("07-程序文件-质量保证与改进.md", [4]),         # 内部审计
    "B2": ("06-程序文件-检验流程.md", [3, 4]),            # 室内质控+室间质评
    "B3": ("07-程序文件-质量保证与改进.md", [4]),         # 内部审计
    "B4": ("07-程序文件-质量保证与改进.md", [5]),         # 管理评审
    "B5": ("07-程序文件-质量保证与改进.md", [3]),         # 纠正措施
    "C1": ("06-程序文件-检验流程.md", [3]),               # 室内质控
    "C2": ("06-程序文件-检验流程.md", [2]),               # 检验方法
    "C3": ("07-程序文件-质量保证与改进.md", [4]),         # 内部审计（体系审查）
    "C4": ("07-程序文件-质量保证与改进.md", [3]),         # 纠正措施
    "C5": ("07-程序文件-质量保证与改进.md", [3]),         # 纠正措施
}


def strip_examples(text: str) -> str:
    lines = text.split("\n")
    result = []
    in_example = False
    for line in lines:
        if "⚠️ 示例" in line:
            in_example = True
            continue
        if in_example:
            if line.startswith(">") or (line.strip() == "" and result and result[-1].strip() == ""):
                continue
            else:
                in_example = False
        result.append(line)
    return "\n".join(result)


def strip_to_skeleton(text: str) -> str:
    """H3 骨架化算法"""
    text = strip_examples(text)
    lines = text.split("\n")
    result = []
    in_table = False
    in_codeblock = False
    lines_after_heading = 0

    for line in lines:
        stripped = line.strip()

        if re.match(r"^#+\s", line):
            result.append(line)
            in_table = False
            lines_after_heading = 0
            continue

        if stripped.startswith(">"):
            continue

        if "|" in line and (stripped.startswith("|") or re.match(r"^\s*\|", line)):
            in_table = True
            continue
        elif in_table and stripped == "":
            in_table = False
            result.append(line)
            continue
        elif in_table:
            continue

        if stripped.startswith("```"):
            in_codeblock = not in_codeblock
            continue
        if in_codeblock:
            continue

        if stripped and not stripped.startswith("-") and not stripped.startswith("1.") and not re.match(r"^\d+\.", stripped):
            if lines_after_heading < 3:
                result.append(line)
                lines_after_heading += 1
            continue

        if stripped == "":
            result.append(line)
            continue

        if re.match(r"^[-\*]\s+", stripped) or re.match(r"^\d+\.\s", stripped):
            if re.search(r"(FM|SOP|REC|JYK|QM|FR)-\S+", stripped):
                result.append(line)
            continue

    cleaned = []
    prev_empty = False
    for line in result:
        is_empty = line.strip() == ""
        if is_empty and prev_empty:
            continue
        cleaned.append(line)
        prev_empty = is_empty
    return "\n".join(cleaned)


def extract_sop(text: str, sop_numbers: list) -> str:
    """从模块中提取指定编号的 SOP"""
    lines = text.split("\n")
    # 找到所有 SOP 标题的位置
    sop_positions = []
    for i, line in enumerate(lines):
        m = re.match(r"^#{1,2}\s+SOP\s*(\d+)", line)
        if m:
            sop_positions.append((i, int(m.group(1))))

    # 提取头部（到第一个 SOP 前）
    if sop_positions:
        header = "\n".join(lines[:sop_positions[0][0]])
    else:
        header = ""

    # 提取指定 SOP
    extracted_sops = []
    for idx, (pos, num) in enumerate(sop_positions):
        if num in sop_numbers:
            end = sop_positions[idx + 1][0] if idx + 1 < len(sop_positions) else len(lines)
            extracted_sops.append("\n".join(lines[pos:end]))

    if not extracted_sops:
        # 如果找不到，返回整个文本（fallback）
        return text

    return header + "\n\n" + "\n\n---\n\n".join(extracted_sops)


def remove_rules_section1(rules_text: str) -> str:
    lines = rules_text.split("\n")
    result = []
    skip = False
    for line in lines:
        if line.strip() == "## 1. 文件结构":
            skip = True
            continue
        if skip and line.startswith("## "):
            skip = False
        if not skip:
            result.append(line)
    return "\n".join(result)


def main():
    with open(f"{DOCS_DIR}/00-使用指南.md") as f:
        guide_raw = f.read()
    with open(f"{FIXES_DIR}/config_restructured/rules.md") as f:
        rules = f.read()
    rules_no_s1 = remove_rules_section1(rules)
    guide_skeleton = strip_to_skeleton(guide_raw)

    stats = []
    for task_id, (module, sop_nums) in TASK_SOP_MAP.items():
        with open(f"{DOCS_DIR}/{module}") as f:
            module_full = f.read()

        # 提取指定 SOP
        sop_text = extract_sop(module_full, sop_nums)
        # 骨架化
        sop_skeleton = strip_to_skeleton(sop_text)

        h4_config = f"{guide_skeleton}\n\n---\n---\n\n{sop_skeleton}\n\n---\n---\n\n# 附加生成规则\n\n{rules_no_s1}"

        h4_path = f"{FIXES_DIR}/configs/H4_{task_id}.txt"
        with open(h4_path, "w") as f:
            f.write(h4_config)

        h4_kb = len(h4_config.encode("utf-8")) / 1024
        stats.append((task_id, h4_kb, module, sop_nums))
        print(f"{task_id}: H4={h4_kb:.0f}K  module={module[:10]}  SOPs={sop_nums}")

    avg = sum(s[1] for s in stats) / len(stats)
    print(f"\nH4 平均: {avg:.0f}K  (对比 H3 平均 13K, G 平均 38K)")


if __name__ == "__main__":
    main()
