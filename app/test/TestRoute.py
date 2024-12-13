# app/test/TestRoute.py

from flask import Blueprint, jsonify, request
import datetime

# 定义Agent路由根目录
test_route = Blueprint('test', __name__)

# 测试用户输入
@test_route.route('/', methods=['GET'])
def test():
    result = {
        "message": "Connection OK.",
        "timestamp": datetime.datetime.now().isoformat()  # 包含时间戳
    }
    return jsonify(result)


import mysql.connector
from config.mysql_config import MYSQL_CONFIG, create_mysql_connection_pool, get_connection_from_pool
@test_route.route('/mysql', methods=['GET'])
def mysql_test():
    try:
        # 创建 MySQL 连接池
        pool = create_mysql_connection_pool()
        # 从连接池中获取连接
        connection = get_connection_from_pool(pool)

        if connection:
            cursor = connection.cursor()

            # SQL 插入语句，向 test 表插入数据
            insert_query = "INSERT INTO test (test) VALUES (%s)"
            cursor.execute(insert_query, ('helloworld',))  # 插入 "helloworld" 到 test_column 列
            print("SQL Query: ", insert_query)
            print("Values: ", ('helloworld',))

            # 提交事务
            connection.commit()

            # 返回成功信息
            result = {
                "message": "Data inserted successfully.",
                "timestamp": datetime.datetime.now().isoformat()
            }
            cursor.close()
            connection.close()
            return jsonify(result)


    except mysql.connector.Error as e:
        result = {
            "message": f"Error occurred: {str(e)}",
            "timestamp": datetime.datetime.now().isoformat()
        }
        return jsonify(result), 500