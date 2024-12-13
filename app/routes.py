from flask import Blueprint, jsonify, request
from app.views.AgentRoute import agent_route
from app.test.TestRoute import test_route
import requests

routes = Blueprint('routes', __name__)

def register_test_routes(app):
    # 注册 test 的路由
    app.register_blueprint(test_route, url_prefix='/test')

def register_agent_routes(app):
    # 注册 Agent 服务的路由
    app.register_blueprint(agent_route, url_prefix='/agent')
