"""
피그마에 표기된대로 후기 관련 정보 반환 유저가 클릭한 파트너의 후기 정보 
user_view_partnerinfo와 결합
"""

from flask import Blueprint, request, jsonify
import logging
import mysql.connector
from db_util import create_db_connection

user_view_partner_reviews_bp = Blueprint('user_view_partner_reviews', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_view_partner_reviews_bp.route('/api/user/partner_reviews', methods=['GET'])
def get_partner_reviews():
    partner_id = request.args.get('partner_id')
    
    if not partner_id:
        logging.error("No partner ID provided")
        return jsonify({"error": "No partner ID provided"}), 400

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch partner reviews
        logging.debug("Fetching partner reviews")
        reviews_query = """
        SELECT r.UID, u.NAME as user_name, u.GENDER as user_gender, r.RATE, r.CONTENT, r.DATE
        FROM REVIEW r
        JOIN USER u ON r.UID = u.UID
        WHERE r.PID = %s
        ORDER BY r.RATE DESC, r.DATE DESC
        """
        cursor.execute(reviews_query, (partner_id,))
        reviews = cursor.fetchall()

        response = {
            "message": "Partner reviews retrieved successfully",
            "reviews": reviews
        }

        return jsonify(response), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()