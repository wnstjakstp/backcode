"""
유저 정기구독 취소 api
"""

from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

user_r_cancel_bp = Blueprint('user_r_cancel', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_r_cancel_bp.route('/api/user/cancel_reservation', methods=['POST'])
def cancel_reservation():
    data = request.json
    reservation_id = data.get('rid')

    if not reservation_id:
        logging.error("Missing reservation ID (rid) parameter")
        return jsonify({"error": "Missing reservation ID (rid) parameter"}), 400

    user_id = session.get('user_id')
    if not user_id:
        logging.error("No user ID in session")
        return jsonify({"error": "No user ID in session"}), 401

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Check if the reservation exists and belongs to the user
        fetch_rid_query = "SELECT RID FROM RESERVATION WHERE UID = %s AND RID = %s"
        cursor.execute(fetch_rid_query, (user_id, reservation_id))
        rid_result = cursor.fetchone()
        
        if not rid_result:
            logging.error("Reservation not found for the given user and reservation ID")
            return jsonify({"error": "Reservation not found"}), 404

        rid = rid_result['RID']

        # Delete from PT_SESSION table
        delete_session_query = "DELETE FROM PT_SESSION WHERE RID = %s"
        cursor.execute(delete_session_query, (rid,))
        session_deleted = cursor.rowcount

        # Delete from RESERVATION table
        delete_reservation_query = "DELETE FROM RESERVATION WHERE RID = %s"
        cursor.execute(delete_reservation_query, (rid,))
        reservation_deleted = cursor.rowcount

        connection.commit()
        
        if reservation_deleted == 0:
            logging.error("Failed to delete the reservation")
            return jsonify({"error": "Failed to delete the reservation"}), 500
        
        if session_deleted == 0:
            logging.warning("No PT sessions found for the reservation")

        logging.debug("Reservation deleted successfully")
        return jsonify({"message": "Reservation deleted successfully"}), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()