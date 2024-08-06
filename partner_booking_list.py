"""
파트너에게 신청한 예약내역의 리스트를 반환 
apply 컬럼을 이용하여 알아서 대기중 0 과 예약확정 1을 나누셈 
"""
from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

partner_booking_list_bp = Blueprint('partner_booking_list', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_booking_list_bp.route('/api/partner/booking_list', methods=['GET'])
def get_booking_list():
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
        
        # 모든 예약 조회
        booking_query = """
        SELECT b.BOOKID, b.PID, b.UID, b.YEAR, b.MONTH, b.DAY, b.TIME, b.APPLY, u.NAME as USER_NAME, u.TEL as USER_TEL
        FROM PT.BOOKING b
        JOIN PT.USER u ON b.UID = u.UID
        WHERE b.PID = %s
        """
        cursor.execute(booking_query, (pid,))
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