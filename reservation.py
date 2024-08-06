"""
유저가 정기 구독을 신청하는 api  
피그마 참고 잘하면 알아서 할 수 있을 것 같음
***빡셈***
"""
from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection
from datetime import datetime, timedelta

reservation_bp = Blueprint('reservation', __name__)
logging.basicConfig(level=logging.DEBUG)

@reservation_bp.route('/api/reservation/register', methods=['POST'])
def register_reservation():
    data = request.json

    required_fields = ['pid', 'fcount', 'fdate']
    for field in required_fields:
        if field not in data:
            logging.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required field: {field}"}), 400

    uid = session.get('user_id')
    if not uid:
        logging.error("No user ID in session")
        return jsonify({"error": "No user ID in session"}), 401

    pid = data['pid']
    fcount = data['fcount']
    fdate = data['fdate']
    
    # Calculate the end date (one month after the start date)
    fdate_obj = datetime.strptime(fdate, '%Y-%m-%d')
    edate_obj = fdate_obj + timedelta(days=30)
    edate = edate_obj.strftime('%Y-%m-%d')

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch price from PINFO table
        price_query = "SELECT PRICE FROM PINFO WHERE PID = %s"
        cursor.execute(price_query, (pid,))
        price_result = cursor.fetchone()
        
        if not price_result:
            logging.error("Price not found for the given PID")
            return jsonify({"error": "Price not found for the given PID"}), 404

        price = price_result['PRICE']
        cost = price * fcount

        query = """INSERT INTO RESERVATION (PID, UID, FDATE, EDATE, FCOUNT, CURRENT_COUNT, COST)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (pid, uid, fdate, edate, fcount, 0, cost)
        cursor.execute(query, values)
        connection.commit()
        
        logging.debug("Reservation registered successfully")
        return jsonify({
            "message": "Reservation registered successfully",
            "reservation": {
                "pid": pid,
                "uid": uid,
                "fdate": fdate,
                "edate": edate,
                "fcount": fcount,
                "current_count": 0,
                "cost": cost
            }
        }), 201
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()