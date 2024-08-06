"""
유저가 예약 취소하는 api
"""

from flask import Blueprint, request, jsonify
import logging
import mysql.connector
from db_util import create_db_connection

user_booking_cancel_bp = Blueprint('user_booking_cancel', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_booking_cancel_bp.route('/api/user/booking_cancel', methods=['POST'])
def cancel_booking_by_user():
    data = request.json
    booking_id = data.get('booking_id')
    
    if not booking_id:
        logging.error("Missing booking_id parameter")
        return jsonify({"error": "Missing booking_id parameter"}), 400

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        
        # 예약 삭제 쿼리
        delete_query = "DELETE FROM BOOKING WHERE BOOKID = %s"
        logging.debug(f"Executing query: {delete_query} with booking_id: {booking_id}")
        cursor.execute(delete_query, (booking_id,))
        connection.commit()

        response = {
            "message": "Booking canceled successfully by user",
            "booking_id": booking_id
        }

        return jsonify(response), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()