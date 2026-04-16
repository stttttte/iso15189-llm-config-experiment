"""
知识层消融实验：生成 H2 和 H3 的配置文件。

H2 (保留示例)：与 G_combined 相同，但保留 ⚠️ 示例段落
  - 测试：模板中的示例内容是帮助 LLM 理解还是让 LLM 照抄？

H3 (骨架版)：与 G_combined 相同，但从模板中只保留章节骨架
  - 删除：blockquote（ISO 原文摘录）、表格、⚠️ 示例
  - 保留：章节标题、每章节首段说明（章节用途）、记录表单列表、条款覆盖自查表章节标题
  - 测试：ISO 原文摘录是必要的还是骨架+规则就够了？
"""

import re

DOCS_DIR = "/Users/liusidi/Desktop/15189/15189-docs"
FIXES_DIR = "/Users/liusidi/Desktop/experiment_fixes"

TASK_MODULE_MAP = {
    "A1": ["04-程序文件-人员管理.md"],
    "A2": ["05-程序文件-设施设备试剂.md"],
    "A3": ["06-程序文件-检验流程.md"],
    "A4": ["03-程序文件-组织与管理.md"],
    "A5": ["05-程序文件-设施设备试剂.md", "09-记录表单清单.md"],
    "B1": ["07-程序文件-质量保证与改进.md"],
    "B2": ["06-程序文件-检验流程.md"],
    "B3": ["07-程序文件-质量保证与改进.md"],
    "B4": ["03-程序文件-组织与管理.md"],
    "B5": ["07-程序文件-质量保证与改进.md"],
    "C1": ["07-程序文件-质量保证与改进.md"],
    "C2": ["06-程序文件-检验流程.md"],
    "C3": ["07-程序文件-质量保证与改进.md"],
    "C4": ["07-程序文件-质量保证与改进.md"],
    "C5": ["07-程序文件-质量保证与改进.md"],
}


def strip_examples(text: str) -> str:
    """剥离 ⚠️ 示例段落（用于 G 和 H3）"""
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
    """
    H3 骨架化：保留章节结构，删除详细内容。
    - 保留：标题、每章节第一段（说明性文字）、记录表单章节的编号列表、附录章节标题
    - 删除：blockquote（ISO 原文）、表格、示例段落、详细步骤列表
    """
    # 先剥离示例
    text = strip_examples(text)

    lines = text.split("\n")
    result = []
    in_table = False
    in_blockquote = False
    skip_until_next_heading = False
    lines_after_heading = 0  # 计数：当前章节标题后的行数

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 标题行：重置状态
        if re.match(r"^#+\s", line):
            result.append(line)
            in_table = False
            in_blockquote = False
            skip_until_next_heading = False
            lines_after_heading = 0
            continue

        # Blockquote（通常是 ISO 条款原文引用）：删除
        if stripped.startswith(">"):
            in_blockquote = True
            continue
        else:
            in_blockquote = False

        # 表格：删除整个表格
        if "|" in line and (stripped.startswith("|") or re.match(r"^\s*\|", line)):
            in_table = True
            continue
        elif in_table and stripped == "":
            in_table = False
            # 允许空行通过
            result.append(line)
            continue
        elif in_table:
            continue

        # 代码块/流程图：删除
        if stripped.startswith("```"):
            # 找到下一个 ``` 跳过整个代码块
            skip_until_next_heading = not skip_until_next_heading
            continue
        if skip_until_next_heading:
            continue

        # 每个章节保留前 3 行非空内容作为说明
        if stripped and not stripped.startswith("-") and not stripped.startswith("1.") and not re.match(r"^\d+\.", stripped):
            if lines_after_heading < 3:
                result.append(line)
                lines_after_heading += 1
            continue

        # 保留空行（维持结构）
        if stripped == "":
            result.append(line)
            continue

        # 数字列表或无序列表：如果是简短的表单/文件清单（如"JYK-FM-XX-XXX"），保留
        if re.match(r"^[-\*]\s+", stripped) or re.match(r"^\d+\.\s", stripped):
            # 如果包含编号（FM/SOP/REC 等），保留（这是结构信息）
            if re.search(r"(FM|SOP|REC|JYK|QM|FR)-\S+", stripped):
                result.append(line)
            # 否则跳过
            continue

    # 合并连续空行
    cleaned = []
    prev_empty = False
    for line in result:
        is_empty = line.strip() == ""
        if is_empty and prev_empty:
            continue
        cleaned.append(line)
        prev_empty = is_empty

    return "\n".join(cleaned)


def remove_rules_section1(rules_text: str) -> str:
    """从 rules.md 中移除 §1 文件结构章节"""
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

    # 为 H2 准备的使用指南：保留示例（与 G 区分）
    guide_with_examples = guide_raw  # 不剥离
    # 为 H3 准备的使用指南：骨架化
    guide_skeleton = strip_to_skeleton(guide_raw)
    # G 用的使用指南（剥离示例）
    guide_g = strip_examples(guide_raw)

    stats = []
    for task_id, modules in TASK_MODULE_MAP.items():
        module_texts_g = []   # G 版：剥离示例
        module_texts_h2 = []  # H2 版：保留示例
        module_texts_h3 = []  # H3 版：骨架化

        for mod in modules:
            with open(f"{DOCS_DIR}/{mod}") as f:
                raw = f.read()
            module_texts_g.append(strip_examples(raw))
            module_texts_h2.append(raw)  # 不剥离
            module_texts_h3.append(strip_to_skeleton(raw))

        def join_mods(texts):
            return "\n\n---\n---\n\n".join(texts)

        g_config = f"{guide_g}\n\n---\n---\n\n{join_mods(module_texts_g)}\n\n---\n---\n\n# 附加生成规则\n\n{rules_no_s1}"
        h2_config = f"{guide_with_examples}\n\n---\n---\n\n{join_mods(module_texts_h2)}\n\n---\n---\n\n# 附加生成规则\n\n{rules_no_s1}"
        h3_config = f"{guide_skeleton}\n\n---\n---\n\n{join_mods(module_texts_h3)}\n\n---\n---\n\n# 附加生成规则\n\n{rules_no_s1}"

        h2_path = f"{FIXES_DIR}/configs/H2_{task_id}.txt"
        h3_path = f"{FIXES_DIR}/configs/H3_{task_id}.txt"
        with open(h2_path, "w") as f:
            f.write(h2_config)
        with open(h3_path, "w") as f:
            f.write(h3_config)

        g_kb = len(g_config.encode("utf-8")) / 1024
        h2_kb = len(h2_config.encode("utf-8")) / 1024
        h3_kb = len(h3_config.encode("utf-8")) / 1024
        stats.append((task_id, g_kb, h2_kb, h3_kb))
        print(f"{task_id}: G={g_kb:.0f}K  H2={h2_kb:.0f}K (+{h2_kb-g_kb:.0f}K examples)  H3={h3_kb:.0f}K ({h3_kb/g_kb*100:.0f}% of G)")

    print(f"\n汇总:")
    print(f"  G   平均: {sum(s[1] for s in stats)/len(stats):.0f}K")
    print(f"  H2  平均: {sum(s[2] for s in stats)/len(stats):.0f}K")
    print(f"  H3  平均: {sum(s[3] for s in stats)/len(stats):.0f}K")


if __name__ == "__main__":
    main()
