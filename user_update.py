# 유저 개인정보 업데이트 

from flask import Blueprint, request, jsonify
import logging
from db_util import create_db_connection

user_update_bp = Blueprint('user_update', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_update_bp.route('/api/user/update', methods=['POST'])
def update_user():
    data = request.json

    # 필수 필드 확인
    required_fields = ['uid']
    for field in required_fields:
        if field not in data:
            logging.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required field: {field}"}), 400

    uid = data['uid']
    pw = data.get('pw')
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    tel = data.get('tel')
    gu = data.get('gu')
    dong = data.get('dong')
    img = data.get('img')
    intro = data.get('intro')

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        # 업데이트할 필드 준비
        update_fields = []
        update_values = []

        if pw:
            update_fields.append("PW = %s")
            update_values.append(pw)
        if name:
            update_fields.append("NAME = %s")
            update_values.append(name)
        if age:
            update_fields.append("AGE = %s")
            update_values.append(age)
        if gender:
            update_fields.append("GENDER = %s")
            update_values.append(gender)
        if tel:
            update_fields.append("TEL = %s")
            update_values.append(tel)
        if gu:
            update_fields.append("GU = %s")
            update_values.append(gu)
        if dong:
            update_fields.append("DONG = %s")
            update_values.append(dong)
        if img:
            update_fields.append("IMG = %s")
            update_values.append(img)
        if intro:
            update_fields.append("INTRO = %s")
            update_values.append(intro)

        if not update_fields:
            logging.error("No fields to update")
            return jsonify({"error": "No fields to update"}), 400

        update_values.append(uid)
        update_query = f"UPDATE USER SET {', '.join(update_fields)} WHERE UID = %s"

        logging.debug("Executing UPDATE query for USER")
        cursor.execute(update_query, update_values)
        connection.commit()

        if cursor.rowcount == 0:
            logging.error("User not found or no changes made")
            return jsonify({"error": "User not found or no changes made"}), 404

        logging.debug("User updated successfully")
        return jsonify({"message": "User updated successfully"}), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.debug("Database connection closed")