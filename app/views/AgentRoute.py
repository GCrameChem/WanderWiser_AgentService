# app/views/AgentRoute.py
from flask import Blueprint, jsonify, request,send_file,send_from_directory
import os
from dotenv import load_dotenv

# 加载环境变量 (如果你使用 .env 文件来设置环境变量)
load_dotenv()

# 获取环境变量
DOWNLOAD_FILE_PATH = os.environ.get('DOWNLOAD_FILE_PATH', 'http://default_path')


# from app.views.Agent.CenterAgent1_1_cmd import user_input

# 定义Agent路由根目录
agent_route = Blueprint('agent', __name__)


# 测试用户输入
from app.views.Agent.agent import echo_input

@agent_route.route('/echoInput', methods=['POST'])
def process_agent_request():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    # 调用具体的 Agent 服务
    result = echo_input(data)
    return jsonify(result)



# 生成概要计划
from app.views.Agent.CenterAgent1_1_input import generate_travel_plan
from utils.generate_md import generate_main_md, generate_daily_md
from langchain_core.output_parsers import StrOutputParser

@agent_route.route('/query/stage1', methods=['POST'])
def agent_request():
    # Get data from the request
    data = request.json
    if not data or 'query' not in data or 'user_id' not in data:
        return jsonify({'error': 'Invalid input, "query" and "user_id" are required.'}), 400

    user_input = data['query']
    user_id = data['user_id']

    try:
        print(user_input)
        print(user_id)
        # 这里假设获取 agent 执行的结果
        result = generate_travel_plan(user_id, user_input)
        # result1 = agent_executor.invoke({
        #     "messages": [("user", user_input)],  # 传递用户输入
        # })
        # "output": messages["messages"][-1].content
        # result = result1["messages"][-1].content  # 返回生成的结果
        print(result)

        # 生成概要计划并返回文件路径
        file_path, title = generate_main_md(user_id, result)
        print(file_path)
        # 如果 result 包含 URL，返回 URL；否则返回空
        if file_path:
            file_url = f"{user_id}/main_plan.md"
            # 假设你的服务器提供该文件的 URL 路径
            return jsonify({'file_url': file_url,'output':title})
        else:
            # 如果不需要生成文件，返回空 URL 或其他合适的响应
            return jsonify({'file_url': None,'output':result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 获取环境变量 STATIC_FOLDER
STATIC_FOLDER = os.environ.get('STATIC_FOLDER')

# 处理文件下载，统一调用下载文件逻辑
@agent_route.route('/download/main_plan1', methods=['POST'])
def download_main_plan1_front():
    # 获取传入的 user_id
    data = request.json
    if not data or 'file_url' not in data:
        return jsonify({'error': 'Invalid input, "file_url" is required.'}), 400

    file_url = data['file_url']
    print(f"Received file URL: {file_url}")

    # 拼接文件的绝对路径
    file_path = os.path.join(STATIC_FOLDER, file_url.replace('\\', '/'))
    print(f"Resolved file path: {file_path}")

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 构建完整的下载 URL
        download_url = f"http://heywanderwiser.com/generated_plans/{file_url.replace('\\', '/')}"
        print(f"Download URL: {download_url}")

        # 使用 send_from_directory 发送文件
        return send_from_directory(STATIC_FOLDER, file_url.replace('\\', '/'), as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

# 处理文件下载，统一调用下载文件逻辑
@agent_route.route('/download/main_plan', methods=['POST'])
def download_main_plan():
    # 获取传入的 file_url
    data = request.json
    if not data or 'file_url' not in data:
        return jsonify({'error': 'Invalid input, "file_url" is required.'}), 400

    file_url = data['file_url']
    print(f"Received file URL: {file_url}")

    # 拼接文件的绝对路径
    file_path = os.path.join(STATIC_FOLDER, file_url.replace('\\', '/'))
    print(f"Resolved file path: {file_path}")

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 打开文件并读取其内容
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # 返回文件内容作为纯文本
        return jsonify({
            "file_content": file_content
        })

    else:
        return jsonify({"error": "File not found"}), 404


# 后端调用函数
def download_main_plan_db(file_url):
    # 拼接文件的绝对路径
    file_path = os.path.join(STATIC_FOLDER, file_url.replace('\\', '/'))
    print(f"Resolved file path: {file_path}")

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 打开文件并读取其内容
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # 返回文件内容作为纯文本
        return jsonify({
            "file_content": file_content
        })

    else:
        return jsonify({"error": "File not found"}), 404







'''
{
    "query": "我和一个朋友想要去成都旅游三天，我们喜欢人文艺术。请你给我们规划一份行程安排。",
    "user_id": "12345"
}


{
    "message": "Plan generated and saved as markdown file.",
    "file_url": "/generated_plans/12345/main_plan.md"
}


'''



# from app.views.Agent.PAEAgent import agent_planner
# @agent_route.route('/query/stage2', methods=['POST'])
# def agent_request():
#     # Get data from the request
#     data = request.json
#     if not data or 'query' not in data or 'user_id' not in data:
#         return jsonify({'error': 'Invalid input, "query" and "user_id" are required.'}), 400
#
#     # 需要传入的参数：user_id和输入
#     user_input = data['query']  # Extract the user input text
#     user_id = data['user_id']  # Extract the user id
#
#     # 将用户输入作为参数传给executor
#     try:
#         result = agent_executor.invoke({
#             "messages": [("user", user_input)],
#         })
#
#         # 假设 result 是包含多个计划的列表，类似于 ['Plan for Day 1', 'Plan for Day 2', ...]
#         print(f"Agent result for user {user_id}: {result}")
#
#         # 将Agent输出写成md文件，返回文件路径列表
#         file_paths = generate_main_md(user_id, result)
#
#         # 向前端发送生成的md文件路径列表
#         return jsonify({'message': 'Plan generated and saved as markdown files.', 'files': file_paths})
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
