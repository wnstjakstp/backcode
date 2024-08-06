"""
유저가 예약을 신청하는 api 
프론트엔드에서 날짜, 시간, 기타 정보를 받아서 book 테이블에 저장해줌 
"""

from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

booking_bp = Blueprint('booking', __name__)
logging.basicConfig(level=logging.DEBUG)

# 예약 등록 API
@booking_bp.route('/api/booking/register', methods=['POST'])
def register_booking():
    data = request.json
    
    required_fields = ['pid', 'year', 'month', 'day', 'time', 'purpose', 'experience', 'preferred_time']
    for field in required_fields:
        if field not in data:
            logging.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    pid = data['pid']
    year = data['year']
    month = data['month']
    day = data['day']
    time = data['time']  # Assuming this is a string in HH:MM format
    purpose = data['purpose']
    experience = data['experience']
    preferred_time = data['preferred_time']
    
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
        
        # 예약 정보 삽입
        query = """INSERT INTO BOOKING (PID, UID, YEAR, MONTH, DAY, TIME, PURPOSE, EXPERIENCE, PRTIME, APPLY)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (pid, uid, year, month, day, time, purpose, experience, preferred_time, 0)
        cursor.execute(query, values)
        connection.commit()
        
        # 예약된 유저 정보 조회
        user_query = "SELECT NAME, TEL FROM USER WHERE UID = %s"
        cursor.execute(user_query, (uid,))
        user_info = cursor.fetchone()
        
        if not user_info:
            logging.error("User not found")
            return jsonify({"error": "User not found"}), 404
        
        # PINFO의 EPRICE 조회
        pinfo_query = "SELECT EPRICE FROM PINFO WHERE PID = %s"
        cursor.execute(pinfo_query, (pid,))
        pinfo_info = cursor.fetchone()
        
        if not pinfo_info:
            logging.error("PINFO not found")
            return jsonify({"error": "PINFO not found"}), 404

        response = {
            "message": "Booking registered successfully",
            "booking_info": {
                "date": f"{year}-{month:02d}-{day:02d}",
                "time": time,
                "eprice": pinfo_info['EPRICE'],
                "user_name": user_info['NAME'],
                "user_tel": user_info['TEL']
            }
        }
        
        logging.debug("Booking registered successfully")
        return jsonify(response), 201
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()