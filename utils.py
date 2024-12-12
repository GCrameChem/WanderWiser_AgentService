# 工具函数

# 输出项目树
import os

def generate_file_structure(path):
    file_structure = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        file_structure += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            file_structure += f"{subindent}{file}\n"
    return file_structure

# 设置工作目录路径
path = '.'  # 当前目录
file_structure = generate_file_structure(path)

# 输出到 README.md 文件
with open('README.md', 'w') as f:
    f.write('# Project File Structure\n')
    f.write('```\n')
    f.write(file_structure)
    f.write('```\n')

print("File structure written to README.md")
