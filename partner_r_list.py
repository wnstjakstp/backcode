"""
파트너 본인에게 구독한 유저들의 리스트를 반환 이름 종료일 표시
현재 횟수 및 예정 횟수 표시 
"""

from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

partner_r_list_bp = Blueprint('partner_r_list', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_r_list_bp.route('/api/partner/r_list', methods=['GET'])
def get_partner_r_list():
    pid = session.get('partner_id')
    
    if not pid:
        logging.error("No partner ID in session")
        return jsonify({"error": "No partner ID in session"}), 401

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        # 파트너의 구독 유저 리스트 조회
        subscription_query = """
        SELECT r.RID, r.UID, r.FDATE, r.EDATE, r.FCOUNT, r.CURRENT_COUNT, r.COST, u.NAME as USER_NAME
        FROM RESERVATION r
        JOIN USER u ON r.UID = u.UID
        WHERE r.PID = %s
        """
        cursor.execute(subscription_query, (pid,))
        subscriptions = cursor.fetchall()

        # 날짜 형식을 YYYY-MM-DD로 변환
        for subscription in subscriptions:
            subscription['FDATE'] = subscription['FDATE'].strftime('%Y-%m-%d')
            subscription['EDATE'] = subscription['EDATE'].strftime('%Y-%m-%d')

        response = {
            "message": "Subscription list retrieved successfully",
            "subscriptions": subscriptions
        }

        return jsonify(response), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()