# Flask应用工厂

from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
from app.routes import routes


load_dotenv()  # 加载环境变量

# Add the myapp directory to sys.path
# Add the myapp directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))


def create_app():
    app = Flask(__name__)

    # Configure MySQL
    app.config.from_mapping(
        SECRET_KEY='dev',
        MYSQL_HOST=os.getenv('MYSQL_HOST'),
        MYSQL_USER=os.getenv('MYSQL_USER'),
        MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD'),
        MYSQL_DB=os.getenv('MYSQL_DB'),
    )

    mysql = MySQL(app)

    # 注册 Blueprint
    app.register_blueprint(routes)
    # 启用跨域请求支持
    CORS(app)


    return app
