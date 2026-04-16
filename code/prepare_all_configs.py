"""
为 15 个任务生成 F_template 和 G_template_rules 的配置文件。
每个任务注入：00-使用指南 + 最相关的模板模块。
"""

import re

DOCS_DIR = "/Users/liusidi/Desktop/15189/15189-docs"
FIXES_DIR = "/Users/liusidi/Desktop/experiment_fixes"

# 任务→模板模块映射
TASK_MODULE_MAP = {
    "A1": ["04-程序文件-人员管理.md"],           # §6.2 人员
    "A2": ["05-程序文件-设施设备试剂.md"],       # §6.4 设备
    "A3": ["06-程序文件-检验流程.md"],           # §5.4/7.x 检验前过程
    "A4": ["03-程序文件-组织与管理.md"],         # §8.9 管理评审（在组织与管理中）
    "A5": ["05-程序文件-设施设备试剂.md", "09-记录表单清单.md"],  # 设备校准记录表
    "B1": ["07-程序文件-质量保证与改进.md"],     # 内审检查表
    "B2": ["06-程序文件-检验流程.md"],           # §7.3 检验过程质控
    "B3": ["07-程序文件-质量保证与改进.md"],     # 迎检自查
    "B4": ["03-程序文件-组织与管理.md"],         # §8.9 管理评审
    "B5": ["07-程序文件-质量保证与改进.md"],     # 整改计划
    "C1": ["07-程序文件-质量保证与改进.md"],     # 审查质控程序
    "C2": ["06-程序文件-检验流程.md"],           # 审查检验SOP
    "C3": ["07-程序文件-质量保证与改进.md"],     # 体系级审查
    "C4": ["07-程序文件-质量保证与改进.md"],     # 审核驱动修改
    "C5": ["07-程序文件-质量保证与改进.md"],     # 整改闭环
}


def strip_examples(text: str) -> str:
    """剥离 ⚠️ 示例段落"""
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
    # 读取使用指南和规则
    with open(f"{DOCS_DIR}/00-使用指南.md") as f:
        guide = strip_examples(f.read())
    with open(f"{FIXES_DIR}/config_restructured/rules.md") as f:
        rules = f.read()
    rules_no_s1 = remove_rules_section1(rules)

    # 为每个任务生成配置
    for task_id, modules in TASK_MODULE_MAP.items():
        # 读取并拼接模块
        module_texts = []
        for mod in modules:
            with open(f"{DOCS_DIR}/{mod}") as f:
                module_texts.append(strip_examples(f.read()))

        module_combined = "\n\n---\n---\n\n".join(module_texts)

        # F_template 配置
        f_config = f"{guide}\n\n---\n---\n\n{module_combined}"

        # G_template_rules 配置
        g_config = f"{f_config}\n\n---\n---\n\n# 附加生成规则\n\n{rules_no_s1}"

        # 写入
        f_path = f"{FIXES_DIR}/configs/F_{task_id}.txt"
        g_path = f"{FIXES_DIR}/configs/G_{task_id}.txt"

        with open(f_path, "w") as f:
            f.write(f_config)
        with open(g_path, "w") as f:
            f.write(g_config)

        f_kb = len(f_config.encode("utf-8")) / 1024
        g_kb = len(g_config.encode("utf-8")) / 1024
        print(f"{task_id}: F={f_kb:.0f}K  G={g_kb:.0f}K  modules={modules}")


if __name__ == "__main__":
    main()
