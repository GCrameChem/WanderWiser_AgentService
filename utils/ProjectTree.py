# 生成项目树

import os

def load_ignore_list(gitignore_path):
    """加载 .gitignore 中的忽略列表"""
    ignore_dirs = []
    if os.path.exists(gitignore_path):
        # 指定编码为 UTF-8
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    ignore_dirs.append(stripped.rstrip('/'))  # 去除尾部斜杠
    return ignore_dirs

def generate_file_structure(path, ignore_dirs=None):
    """生成项目目录树"""
    if ignore_dirs is None:
        ignore_dirs = []

    file_structure = ""
    for root, dirs, files in os.walk(path):
        # 过滤忽略的目录
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        file_structure += f"{indent}{os.path.basename(root)}/\n"

        subindent = ' ' * 4 * (level + 1)
        for file in files:
            file_structure += f"{subindent}{file}\n"

    return file_structure
