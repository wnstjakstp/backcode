# partner_login.py
# 파트너 로그인
from flask import Blueprint, request, jsonify, session
import logging
import base64
from db_util import create_db_connection  # db_util에서 create_db_connection 임포트

partner_login_bp = Blueprint('partner_login', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_login_bp.route('/api/partner/login', methods=['POST'])
def login():
    data = request.json

    if 'pid' not in data or 'pw' not in data:
        logging.error("Missing required fields: pid or pw")
        return jsonify({"error": "Missing required fields: pid or pw"}), 400

    pid = data['pid']
    pw = data['pw']

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        logging.debug("Executing SELECT query")
        query = "SELECT * FROM PARTNER WHERE PID = %s AND PW = %s"
        cursor.execute(query, (pid, pw))
        partner = cursor.fetchone()

        if partner:
            session['partner_id'] = partner['PID']
            partner['IMG'] = base64.b64encode(partner['IMG']).decode('utf-8') if partner['IMG'] else None
            logging.debug("Partner logged in successfully")
            return jsonify(partner), 200
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