# user_login.py
from flask import Blueprint, request, jsonify, session
import logging
import base64
from db_util import create_db_connection  # db_util에서 create_db_connection 임포트

user_login_bp = Blueprint('user_login', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_login_bp.route('/api/user/login', methods=['POST'])
def login():
    data = request.json

    if 'uid' not in data or 'pw' not in data:
        logging.error("Missing required fields: uid or pw")
        return jsonify({"error": "Missing required fields: uid or pw"}), 400

    uid = data['uid']
    pw = data['pw']

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        logging.debug("Executing SELECT query")
        query = "SELECT * FROM USER WHERE UID = %s AND PW = %s"
        cursor.execute(query, (uid, pw))
        user = cursor.fetchone()

        if user:
            # 프로필 이미지를 Base64로 인코딩
            user['IMG'] = base64.b64encode(user['IMG']).decode('utf-8') if user['IMG'] else None
            session['user_id'] = user['UID']
            logging.debug("User logged in successfully")
            return jsonify(user), 200
        else:
            logging.error("Invalid credentials")
            return jsonify({"error": "Invalid credentials"}), 401
    except Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.debug("Database connection closed")