import os
from utils.ProjectTree import load_ignore_list, generate_file_structure

# 设置项目路径和 .gitignore 路径
PROJECT_ROOT = '.'
GITIGNORE_PATH = os.path.join(PROJECT_ROOT, '.gitignore')

# 加载忽略列表
ignore_dirs = load_ignore_list(GITIGNORE_PATH)

# 生成文件结构
file_structure = generate_file_structure(PROJECT_ROOT, ignore_dirs=ignore_dirs)

# 输出到 README.md 文件
README_PATH = os.path.join(PROJECT_ROOT, 'README.md')
with open(README_PATH, 'w') as f:
    f.write('# Project File Structure\n')
    f.write('```\n')
    f.write(file_structure)
    f.write('```\n')

print(f"File structure written to {README_PATH}")
