"""
예약 신청 디테일 페이지 
유저와 파트너가 공유 
"""
from flask import Blueprint, request, jsonify
import logging
import mysql.connector
from db_util import create_db_connection

booking_detail_bp = Blueprint('booking_detail', __name__)
logging.basicConfig(level=logging.DEBUG)

@booking_detail_bp.route('/api/booking_detail', methods=['GET'])
def get_booking_detail():
    book_id_param = request.args.get('book_id')
    
    if not book_id_param:
        logging.error("Missing book_id parameter")
        return jsonify({"error": "Missing book_id parameter"}), 400

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        logging.debug(f"Fetching booking details for book_id: {book_id_param}")
        booking_query = """
        SELECT b.BOOKID, b.PID, b.UID, b.YEAR, b.MONTH, b.DAY, b.TIME, b.PURPOSE,
               b.EXPERIENCE, b.PRTIME, b.APPLY,
               p.NAME as PARTNER_NAME, p.TEL as PARTNER_TEL,
               u.NAME as USER_NAME, u.TEL as USER_TEL
        FROM BOOKING b
        JOIN PARTNER p ON b.PID = p.PID
        JOIN USER u ON b.UID = u.UID
        WHERE b.BOOKID = %s
        """
        cursor.execute(booking_query, (book_id_param,))
        booking_info = cursor.fetchone()

        if not booking_info:
            return jsonify({"error": "Booking not found"}), 404

        response = {
            "message": "Booking detail retrieved successfully",
            "booking_info": {
                "BOOKID": booking_info["BOOKID"],
                "PARTNER_NAME": booking_info["PARTNER_NAME"],
                "PARTNER_TEL": booking_info["PARTNER_TEL"],
                "USER_NAME": booking_info["USER_NAME"],
                "USER_TEL": booking_info["USER_TEL"],
                "YEAR": booking_info["YEAR"],
                "MONTH": booking_info["MONTH"],
                "DAY": booking_info["DAY"],
                "TIME": booking_info["TIME"],
                "PURPOSE": booking_info["PURPOSE"],
                "EXPERIENCE": booking_info["EXPERIENCE"],
                "PRTIME": booking_info["PRTIME"],
                "APPLY": booking_info["APPLY"]
            }
        }

        return jsonify(response), 200

    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()