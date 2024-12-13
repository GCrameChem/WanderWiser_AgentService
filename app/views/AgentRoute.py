from flask import Blueprint, jsonify, request,send_file
import os

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
from app.views.Agent.CenterAgent1_1_input import agent_executor
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
        print("request OK")
        # 这里假设获取 agent 执行的结果

        result1 = agent_executor.invoke({
            "messages": [("user", user_input)],  # 传递用户输入
        })
        # "output": messages["messages"][-1].content
        result = result1["messages"][-1].content  # 返回生成的结果
        print(result)

        # 生成概要计划并返回文件路径
        file_path = generate_main_md(user_id, result)
        print(file_path)
        # 如果 result 包含 URL，返回 URL；否则返回空
        if file_path:
            file_url = f"./generated_plans/{user_id}/main_plan.md"  # 假设你的服务器提供该文件的 URL 路径
            return jsonify({'file_url': file_url,'output':result})
        else:
            # 如果不需要生成文件，返回空 URL 或其他合适的响应
            return jsonify({'file_url': None,'output':result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 假设存在一个路由用来处理文件下载
@agent_route.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join('./generated_plans', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
        return jsonify({'error': 'File not found.'}), 404




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
