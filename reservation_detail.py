"""
정기 구독 상세정보 제공 api 
유저와 파트너에게 모두 사용가능 api 
"""

from flask import Blueprint, request, jsonify
import logging
import mysql.connector
from db_util import create_db_connection
from datetime import datetime

reservation_detail_bp = Blueprint('reservation_detail', __name__)
logging.basicConfig(level=logging.DEBUG)

@reservation_detail_bp.route('/api/reservation_detail', methods=['GET'])
def get_reservation_detail():
    rid_param = request.args.get('rid')
    
    if not rid_param:
        logging.error("Missing rid parameter")
        return jsonify({"error": "Missing rid parameter"}), 400

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        # Fetch reservation details
        logging.debug(f"Fetching reservation details for rid: {rid_param}")
        reservation_query = """
        SELECT r.RID, r.PID, r.UID, r.FCOUNT, r.FDATE, r.EDATE, r.CURRENT_COUNT, r.COST,
               p.NAME as PARTNER_NAME, i.GNAME as GYM_NAME, i.PRICE, u.NAME as USER_NAME
        FROM RESERVATION r
        JOIN PARTNER p ON r.PID = p.PID
        JOIN PINFO i ON r.PID = i.PID
        JOIN USER u ON r.UID = u.UID
        WHERE r.RID = %s
        """
        cursor.execute(reservation_query, (rid_param,))
        reservation_info = cursor.fetchone()

        if not reservation_info:
            return jsonify({"error": "Reservation not found"}), 404

        # Fetch PT session details
        pt_session_query = "SELECT CHECK_DATE FROM PT_SESSION WHERE RID = %s ORDER BY CHECK_DATE ASC"
        cursor.execute(pt_session_query, (reservation_info['RID'],))
        pt_sessions = cursor.fetchall()

        # Format PT session details
        pt_session_list = [{"No": idx+1, "CHECK_DATE": session["CHECK_DATE"].strftime('%Y-%m-%d')} for idx, session in enumerate(pt_sessions)]

        # Calculate remaining sessions
        remaining_sessions = reservation_info['FCOUNT'] - reservation_info['CURRENT_COUNT']

        response = {
            "message": "Reservation detail retrieved successfully",
            "reservation_info": {
                "PARTNER_NAME": reservation_info["PARTNER_NAME"],
                "USER_NAME": reservation_info["USER_NAME"],
                "GYM_NAME": reservation_info["GYM_NAME"],
                "PRICE": reservation_info["PRICE"],
                "FCOUNT": reservation_info["FCOUNT"],
                "REMAINING_SESSIONS": remaining_sessions,
                "FDATE": reservation_info["FDATE"].strftime('%Y-%m-%d'),
                "EDATE": reservation_info["EDATE"].strftime('%Y-%m-%d'),
                "CURRENT_COUNT": reservation_info["CURRENT_COUNT"],
                "COST": reservation_info["COST"],
                "PT_SESSIONS": pt_session_list
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