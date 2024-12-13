# config/mysql_config.py

import os
from dotenv import load_dotenv
# import pymysql
# pymysql.install_as_MySQLdb()  # 这会让 PyMySQL 作为 MySQLdb 模块来使用

import mysql.connector

# Load environment variables from .env file
load_dotenv()

# Define MySQL configuration
MYSQL_CONFIG = {
    "host": os.getenv('MYSQL_HOST'),
    "user": os.getenv('MYSQL_USER'),
    "password": os.getenv('MYSQL_PASSWORD'),
    "db": os.getenv('MYSQL_DB'),
    "pool_name": "travel_plan_pool",
    "pool_size": 5  # Define the size of your connection pool
}

import mysql.connector
from mysql.connector import pooling

def create_mysql_connection_pool():
    try:
        # 创建 MySQL 连接池
        pool = pooling.MySQLConnectionPool(
            pool_name=MYSQL_CONFIG["pool_name"],
            pool_size=5,
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["db"]
        )
        return pool
    except mysql.connector.Error as e:
        print(f"Error creating connection pool: {e}")
        raise

# def create_mysql_connection_pool():
#     try:
#         pool = mysql.connector.MySQLConnectionPool(
#             pool_name=MYSQL_CONFIG["pool_name"],
#             pool_size=MYSQL_CONFIG["pool_size"],
#             host=MYSQL_CONFIG["host"],
#             user=MYSQL_CONFIG["user"],
#             password=MYSQL_CONFIG["password"],
#             database=MYSQL_CONFIG["db"]
#         )
#         return pool
#     except mysql.connector.Error as e:
#         print(f"Error creating connection pool: {e}")
#         raise

# Use the connection pool to execute SQL queries
def get_connection_from_pool(pool):
    try:
        connection = pool.get_connection()
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error getting connection from pool: {e}")
        raise