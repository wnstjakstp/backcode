"""
유저 신청 목록 반환 대기 0과 수락 1로 나눠서 반영하셈
"""
from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

user_booking_list_bp = Blueprint('user_booking_list', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_booking_list_bp.route('/api/user/booking_list', methods=['GET'])
def get_user_booking_list():
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
        
        # 유저의 예약 내역 조회
        booking_query = """
        SELECT b.BOOKID, b.PID, b.UID, b.YEAR, b.MONTH, b.DAY, b.TIME, b.APPLY, 
               p.NAME as PARTNER_NAME, i.GNAME as GYM_NAME, i.PRICE
        FROM BOOKING b
        JOIN PARTNER p ON b.PID = p.PID
        JOIN PINFO i ON b.PID = i.PID
        WHERE b.UID = %s
        """
        cursor.execute(booking_query, (uid,))
        bookings = cursor.fetchall()

        response = {
            "message": "Booking list retrieved successfully",
            "bookings": bookings
        }

        return jsonify(response), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()