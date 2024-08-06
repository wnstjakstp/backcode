"""
파트너가 PT마치고 횟수 체크하면 PT_SESSION 테이블에 날짜가 기록됨 unique로 같은날짜
체크 안되게 중복 방지 걸어놓음
추가로 current_count가 오름 
추가로 fcount -current_count -> 로 남은 횟수도 같이 반환
잘 되는거 확인함 
"""
from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection
from datetime import datetime

partner_check_session_bp = Blueprint('partner_check_session', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_check_session_bp.route('/api/partner/check_session', methods=['POST'])
def check_session():
    data = request.json
    rid = data.get('rid')

    if not rid:
        logging.error("Missing reservation ID (rid) parameter")
        return jsonify({"error": "Missing reservation ID (rid) parameter"}), 400

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

        # Check if the reservation exists
        reservation_query = "SELECT * FROM RESERVATION WHERE RID = %s AND PID = %s"
        cursor.execute(reservation_query, (rid, pid))
        reservation = cursor.fetchone()
        
        if not reservation:
            logging.error("No reservation found for the given RID and PID")
            return jsonify({"error": "No reservation found for the given RID and PID"}), 404

        # Check for duplicate date
        check_date = datetime.now().strftime('%Y-%m-%d')
        duplicate_check_query = "SELECT * FROM PT_SESSION WHERE RID = %s AND CHECK_DATE = %s"
        cursor.execute(duplicate_check_query, (rid, check_date))
        duplicate = cursor.fetchone()
        
        if duplicate:
            logging.error("Duplicate check-in for the same date")
            return jsonify({"error": "Duplicate check-in for the same date"}), 400
        
        # Update CURRENT_COUNT in RESERVATION table
        update_query = "UPDATE RESERVATION SET CURRENT_COUNT = CURRENT_COUNT + 1 WHERE RID = %s"
        cursor.execute(update_query, (rid,))
        
        # Insert new session record in PT_SESSION table
        insert_session_query = "INSERT INTO PT_SESSION (RID, CHECK_DATE) VALUES (%s, %s)"
        cursor.execute(insert_session_query, (rid, check_date))
        
        connection.commit()

        # Fetch updated reservation details
        reservation_query = "SELECT * FROM RESERVATION WHERE RID = %s"
        cursor.execute(reservation_query, (rid,))
        reservation_details = cursor.fetchone()
        
        logging.debug("Session checked successfully")
        return jsonify({"message": "Session checked successfully", "reservation_details": reservation_details}), 201
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()