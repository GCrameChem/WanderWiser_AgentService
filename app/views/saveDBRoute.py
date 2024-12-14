from flask import Blueprint, jsonify, request,send_file
import os
from dotenv import load_dotenv

# 加载环境变量 (如果你使用 .env 文件来设置环境变量)
load_dotenv()


# 定义Agent路由根目录
saveDB_route = Blueprint('saveDB', __name__)

@saveDB_route.route('/test', methods=['POST'])
def test_save_DB():
    print(request.data)
    return jsonify({'notice': 'connected'})

