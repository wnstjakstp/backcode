# partner_register.py
# 파트너 회원가입 
from flask import Blueprint, request, jsonify
import logging
from db_util import create_db_connection  # db_util에서 create_db_connection 임포트
partner_register_bp = Blueprint('partner_register', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_register_bp.route('/api/partner/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    img_file = request.files.get('img')
    print ("AAFasg")
    print ("AAFasg")
    print ("AAFasg")

    if not data:
        logging.error("No data received")
        return jsonify({"error": "No data received"}), 400

    if 'pid' not in data or 'pw' not in data:
        logging.error("Missing required fields: pid or pw")
        return jsonify({"error": "Missing required fields: pid or pw"}), 400

    img_data = None
    if img_file:
        img_data = img_file.read()

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        logging.debug("Executing INSERT query")
        query = """INSERT INTO PARTNER (PID, PW, NAME, AGE, GENDER, TEL, GU, DONG, IMG, ROLE) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            data['pid'],
            data['pw'],
            data.get('name', ''),
            data.get('age', ''),
            data.get('gender', ''),
            data.get('tel', ''),
            data.get('gu', ''),
            data.get('dong', ''),
            img_data,
            '1'  # ROLE 값을 기본값으로 1으로 설정
        )
        cursor.execute(query, values)
        connection.commit()
        logging.debug("Partner registered successfully")
        return jsonify({"message": "Partner registered successfully"}), 201
    except Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.debug("Database connection closed")