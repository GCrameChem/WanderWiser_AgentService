# 启动脚本
from flask import Flask
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
import sys
from app import create_app

# Add the myapp directory to sys.path (use absolute path)
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# print("Current working directory:", os.getcwd())
# print("Project root contents:", os.listdir())