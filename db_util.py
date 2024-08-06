#db설정 파일

import mysql.connector
from mysql.connector import Error
import logging
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

def create_db_connection():
    try:
        logging.debug("Connecting to MySQL database...")
        connection = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            charset='utf8mb4',  # 여기서 문자셋 설정
            collation='utf8mb4_unicode_ci'  # 추가 설정
        )
        logging.debug("Connection established")
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL database: {e}")
        return None