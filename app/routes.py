from flask import Blueprint, request, jsonify
from app.views.agent import run_agent  # 导入 Agent 服务的启动函数

routes = Blueprint('routes', __name__)

# 检测输入
@routes.route('/agent/test', methods=['POST'])
def agent_test():
    try:
        # 从请求中获取传入的文本
        user_input = request.json.get('text', '')
        if not user_input:
            return jsonify({'error': 'No input text provided'}), 400

        # 调用 Agent 的服务处理文本
        response = run_agent(user_input)

        # 返回 Agent 的响应
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 用户普通输入
from views import CenterAgent_main

@routes.route('/agent/query', methods=['POST'])
def agent_query():
    try:
        # 从请求中获取用户输入
        user_input = request.json.get("input", "")
        if not user_input:
            return jsonify({"error": "Input is required"}), 400

        # 启动 CenterAgent 并传入用户输入
        agent_instance = CenterAgent_main()
        response = agent_instance.process_input(user_input)

        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500