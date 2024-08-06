"""
파트너가 유저의 신청을 수락하는 api 
시간 변경을 원하면 바꾸고 수락 아니면 그냥 수락
apply 컬럼이 1로 바뀌면서 확정가능(+시간도 db에 업데이트) 
"""
from flask import Blueprint, request, jsonify
import logging
import mysql.connector
from db_util import create_db_connection

partner_booking_submit_bp = Blueprint('partner_booking_submit', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_booking_submit_bp.route('/api/partner/booking_submit', methods=['POST'])
def submit_booking():
    data = request.json
    booking_id = data.get('booking_id')
    new_year = data.get('year')
    new_month = data.get('month')
    new_day = data.get('day')
    new_time = data.get('time')
    
    if not booking_id:
        logging.error("Missing booking_id parameter")
        return jsonify({"error": "Missing booking_id parameter"}), 400

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        
        # 예약 시간 업데이트 쿼리
        update_query = "UPDATE PT.BOOKING SET APPLY = 1"
        query_values = []
        
        if new_year:
            update_query += ", YEAR = %s"
            query_values.append(new_year)
        if new_month:
            update_query += ", MONTH = %s"
            query_values.append(new_month)
        if new_day:
            update_query += ", DAY = %s"
            query_values.append(new_day)
        if new_time:
            update_query += ", TIME = %s"
            query_values.append(new_time)
        
        update_query += " WHERE BOOKID = %s"
        query_values.append(booking_id)
        
        logging.debug(f"Executing query: {update_query} with values: {query_values}")
        cursor.execute(update_query, query_values)
        connection.commit()

        response = {
            "message": "Booking submitted successfully",
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