# Flask应用工厂

from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config.mysql_config import MYSQL_CONFIG

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

    # 启用跨域支持x
    CORS(app)

    return app

