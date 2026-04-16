"""
预处理脚本：从 15189-docs 模板中提取实验配置文件。

F_template: 00-使用指南 + 04-人员管理(SOP2+SOP3)，剥离示例段落
G_template_rules: F_template + rules.md（去掉§1文件结构，保留术语/模糊/条款等规则）
"""

import re

DOCS_DIR = "/Users/liusidi/Desktop/15189/15189-docs"
FIXES_DIR = "/Users/liusidi/Desktop/experiment_fixes"


def strip_examples(text: str) -> str:
    """剥离 ⚠️ 示例段落（从 > ⚠️ 开始到下一个非引用行）"""
    lines = text.split("\n")
    result = []
    in_example = False
    for line in lines:
        if "⚠️ 示例" in line:
            in_example = True
            continue
        if in_example:
            # 引用块继续（以 > 开头或空行后紧接 >）
            if line.startswith(">") or (line.strip() == "" and result and result[-1].strip() == ""):
                continue
            else:
                in_example = False
        result.append(line)
    return "\n".join(result)


def extract_section(text: str, start_marker: str, end_marker: str | None) -> str:
    """提取两个标记之间的内容"""
    lines = text.split("\n")
    start_idx = None
    end_idx = len(lines)
    for i, line in enumerate(lines):
        if start_marker in line and start_idx is None:
            start_idx = i
        elif end_marker and end_marker in line and start_idx is not None:
            end_idx = i
            break
    if start_idx is None:
        return ""
    return "\n".join(lines[start_idx:end_idx])


def remove_rules_section1(rules_text: str) -> str:
    """从 rules.md 中移除 §1 文件结构章节，保留其余规则"""
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
    # 读取源文件
    with open(f"{DOCS_DIR}/00-使用指南.md") as f:
        guide = f.read()
    with open(f"{DOCS_DIR}/04-程序文件-人员管理.md") as f:
        per_full = f.read()
    with open(f"{FIXES_DIR}/config_restructured/rules.md") as f:
        rules = f.read()

    # 1. 处理使用指南：保留检验科基本信息模板 + 文件格式规范 + LLM通用指令
    #    剥离示例
    guide_clean = strip_examples(guide)

    # 2. 从 04 文件中提取统一格式说明 + SOP 2 + SOP 3
    header = extract_section(per_full, "# 04 程序文件", "# SOP 1")
    sop2 = extract_section(per_full, "# SOP 2", "# SOP 3")
    sop3 = extract_section(per_full, "# SOP 3", "# SOP 4")

    # 剥离示例
    header_clean = strip_examples(header)
    sop2_clean = strip_examples(sop2)
    sop3_clean = strip_examples(sop3)

    # 3. 组装 F_template 配置
    f_config = f"""{guide_clean}

---
---

{header_clean}

---

{sop2_clean}

---

{sop3_clean}
"""

    # 4. 组装 G_template_rules 配置（F + rules without §1）
    rules_no_structure = remove_rules_section1(rules)
    g_config = f"""{f_config}

---
---

# 附加生成规则

{rules_no_structure}
"""

    # 写入文件
    f_path = f"{FIXES_DIR}/F_template_config.txt"
    g_path = f"{FIXES_DIR}/G_template_rules_config.txt"

    with open(f_path, "w") as f:
        f.write(f_config)
    with open(g_path, "w") as f:
        f.write(g_config)

    # 统计
    f_size = len(f_config.encode("utf-8"))
    g_size = len(g_config.encode("utf-8"))
    print(f"F_template_config.txt: {f_size:,} bytes ({f_size/1024:.1f} KB)")
    print(f"G_template_rules_config.txt: {g_size:,} bytes ({g_size/1024:.1f} KB)")
    print(f"rules (no §1): {len(rules_no_structure.encode('utf-8')):,} bytes")


if __name__ == "__main__":
    main()
