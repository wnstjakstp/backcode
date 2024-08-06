"""
유저 정기 목록 반환
"""

from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

user_r_list_bp = Blueprint('user_r_list', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_r_list_bp.route('/api/user/r_list', methods=['GET'])
def get_user_r_list():
    uid = session.get('user_id')
    
    if not uid:
        logging.error("No user ID in session")
        return jsonify({"error": "No user ID in session"}), 401

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        # 유저의 예약 리스트 조회
        reservation_query = """
        SELECT r.RID, r.PID, r.FDATE, r.EDATE, r.FCOUNT, r.CURRENT_COUNT, r.COST, 
               p.NAME as PARTNER_NAME, i.GNAME as GYM_NAME
        FROM RESERVATION r
        JOIN PARTNER p ON r.PID = p.PID
        JOIN PINFO i ON r.PID = i.PID
        WHERE r.UID = %s
        """
        cursor.execute(reservation_query, (uid,))
        reservations = cursor.fetchall()

        # 날짜 형식을 YYYY-MM-DD로 변환
        for reservation in reservations:
            reservation['FDATE'] = reservation['FDATE'].strftime('%Y-%m-%d')
            reservation['EDATE'] = reservation['EDATE'].strftime('%Y-%m-%d')

        response = {
            "message": "Reservation list retrieved successfully",
            "reservations": reservations
        }

        return jsonify(response), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()