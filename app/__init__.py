# Flask应用工厂

from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config.mysql_config import MYSQL_CONFIG
from flask import send_from_directory, jsonify, request

load_dotenv()  # 加载环境变量

def create_app():
    app = Flask(__name__)

    # 导入MySQL配置
    # app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['MYSQL_HOST'] = MYSQL_CONFIG['host']
    app.config['MYSQL_USER'] = MYSQL_CONFIG['user']
    app.config['MYSQL_PASSWORD'] = MYSQL_CONFIG['password']
    app.config['MYSQL_DB'] = MYSQL_CONFIG['db']

    # 初始化 MySQL
    mysql = MySQL(app)

    # 在此处注册路由
    with app.app_context():
        from app.routes import register_agent_routes
        register_agent_routes(app)

        from app.routes import register_test_routes
        register_test_routes(app)

        from app.routes import register_saveDB_routes
        register_saveDB_routes(app)

    # 启用跨域支持x
    CORS(app)

    # 设置静态文件目录
    STATIC_FOLDER = os.environ.get('STATIC_FOLDER')

    # 暴露静态文件目录
    @app.route('/generated_plans/<path:filename>', methods=['GET'])
    def download_file(filename):
        file_path = os.path.join(STATIC_FOLDER, filename)

        # 确保文件存在
        if os.path.exists(file_path):
            return send_from_directory(STATIC_FOLDER, filename, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404

    if __name__ == '__main__':
        app.run(debug=True)

    return app

