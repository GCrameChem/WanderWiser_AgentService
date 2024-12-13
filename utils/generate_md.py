# 将Agent输出结果写为.md文件

import os


def generate_main_md(user_id, result):
    # Check if the first line of result is "Situation3"
    if result.splitlines()[0] != "Situation3":
        # If not, return None (do not generate the markdown file)
        return None

    # Define the path where the markdown file will be saved
    file_path = f"./generated_plans/{user_id}/main_plan.md"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Remove the first line ("Situation3") and join the rest of the content
    content_to_write = "\n".join(result.splitlines()[1:])

    # Write the content to the markdown file (starting from the second line)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content_to_write)

    return file_path


def generate_daily_md(user_id, result):
    """
    生成主行程计划并保存为多个Markdown文件。

    参数:
    user_id (str): 用户的唯一ID
    result (list): 包含多个旅行计划的列表，每个计划代表一天的行程
    """
    # 创建用户文件夹，如果不存在
    user_dir = os.path.join("generated_plans", str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    # 文件列表，用于返回给前端
    file_paths = []

    # 假设 result 是一个列表，其中每个元素代表一天的行程计划
    for i, day_plan in enumerate(result):
        day = f"Day {i + 1}"
        # 构造文件名，例如 "Day1.md", "Day2.md", ...
        file_name = f"{day}.md"
        file_path = os.path.join(user_dir, file_name)

        # 生成Markdown内容
        md_content = f"# {day}\n\n{day_plan}\n"

        # 写入Markdown文件
        with open(file_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_content)

        # 添加文件路径到列表
        file_paths.append(file_path)

    # 输出所有文件路径
    print(f"Generated Markdown files: {file_paths}")

    # 返回文件路径列表
    return file_paths
