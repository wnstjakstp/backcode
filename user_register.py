# user_register.py
from flask import Blueprint, request, jsonify
import logging
from db_util import create_db_connection  # db_util에서 create_db_connection 임포트

user_register_bp = Blueprint('user_register', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_register_bp.route('/api/user/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    img_file = request.files.get('img')

    if not data:
        logging.error("No data received")
        return jsonify({"error": "No data received"}), 400

    if 'uid' not in data or 'pw' not in data:
        logging.error("Missing required fields: uid or pw")
        return jsonify({"error": "Missing required fields: uid or pw"}), 400

    img_data = None
    if img_file:
        img_data = img_file.read()
        logging.debug(f"Image file received: {len(img_data)} bytes")

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        logging.debug("Executing INSERT query")
        query = """INSERT INTO USER (UID, PW, NAME, AGE, GENDER, TEL, GU, DONG, IMG, INTRO, ROLE) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            data['uid'],
            data['pw'],
            data.get('name', ''),
            data.get('age', ''),
            data.get('gender', ''),
            data.get('tel', ''),
            data.get('gu', ''),
            data.get('dong', ''),
            img_data,
            data.get('intro', ''),
            '0'  # ROLE 값을 기본값으로 0으로 설정
        )
        cursor.execute(query, values)
        connection.commit()
        logging.debug("User registered successfully")
        return jsonify({"message": "User registered successfully"}), 201
    except Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.debug("Database connection closed")