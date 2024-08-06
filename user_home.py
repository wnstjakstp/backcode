# user_home.py
# 유저가 홈화면 들어가면 보이는 파트너 리스트 반환
from flask import Blueprint, request, jsonify
import logging
from db_util import create_db_connection

user_home_bp = Blueprint('user_home', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_home_bp.route('/api/user/home', methods=['POST'])
def get_partners_by_location():
    data = request.json

    if 'uid' not in data:
        logging.error("Missing required field: uid")
        return jsonify({"error": "Missing required field: uid"}), 400

    uid = data['uid']

    connection = create_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # 유저의 동 정보 조회
        logging.debug("Executing SELECT query for user location")
        cursor.execute("SELECT DONG FROM USER WHERE UID = %s", (uid,))
        user_info = cursor.fetchone()
        
        if not user_info or 'DONG' not in user_info:
            logging.error("User or location not found")
            return jsonify({"error": "User or location not found"}), 404

        dong = user_info['DONG']

        # 특정 동네의 파트너들 조회
        logging.debug("Executing SELECT query for partners in the specified location")
        query = """
        SELECT p.PID, pt.NAME as trainer_name, p.INTRO as trainer_intro, p.PRICE as price, p.EPRICE as eprice,
               g.NAME as gym_name, COALESCE(AVG(r.RATE), 0) AS avg_rate, COUNT(r.REID) AS review_count,
               p.EXPERT1 as expert1, p.EXPERT2 as expert2, p.IMG as trainer_img
        FROM PINFO p
        JOIN PARTNER pt ON p.PID = pt.PID
        JOIN GYM g ON p.GNAME = g.NAME
        LEFT JOIN REVIEW r ON p.PID = r.PID
        WHERE pt.DONG = %s
        GROUP BY p.PID, pt.NAME, g.NAME
        ORDER BY avg_rate DESC, review_count DESC
        """
        cursor.execute(query, (dong,))
        partners = cursor.fetchall()

        if not partners:
            return jsonify({"message": "No partners found for the given location"}), 404

        return jsonify(partners), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()