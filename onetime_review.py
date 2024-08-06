"""
1회 체험 후기 작성 
sep 컬럼 0으로 지정
행 삽입 시 현재 날짜가 date로 반영
"""

from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection
from datetime import datetime

onetime_review_bp = Blueprint('onetime_review', __name__)
logging.basicConfig(level=logging.DEBUG)

@onetime_review_bp.route('/api/review/one_time', methods=['POST'])
def one_time_review():
    data = request.json
    
    required_fields = ['pid', 'rate', 'content']
    for field in required_fields:
        if field not in data:
            logging.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    pid = data['pid']
    rate = data['rate']
    content = data['content']
    
    uid = session.get('user_id')
    if not uid:
        logging.error("No user ID in session")
        return jsonify({"error": "No user ID in session"}), 401
    
    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor()
        today = datetime.today().strftime('%Y-%m-%d')
        query = """INSERT INTO REVIEW (PID, UID, RATE, CONTENT, SEP, DATE)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (pid, uid, rate, content, 0, today)
        cursor.execute(query, values)
        connection.commit()
        
        logging.debug("One-time review added successfully")
        return jsonify({"message": "One-time review added successfully"}), 201
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()