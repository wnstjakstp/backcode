# 파트너 프로필 업데이트 
from flask import Blueprint, request, jsonify
import logging
from db_util import create_db_connection
import mysql.connector

partner_update_bp = Blueprint('partner_update', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_update_bp.route('/api/partner/update', methods=['POST'])
def update_partner():
    data = request.json

    # 필수 필드 확인
    required_fields = ['pid']
    for field in required_fields:
        if field not in data:
            logging.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required field: {field}"}), 400

    pid = data['pid']
    pw = data.get('pw')
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    tel = data.get('tel')
    gu = data.get('gu')
    dong = data.get('dong')
    img = data.get('img')

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

        if not update_fields:
            logging.error("No fields to update")
            return jsonify({"error": "No fields to update"}), 400

        update_values.append(pid)
        update_query = f"UPDATE PARTNER SET {', '.join(update_fields)} WHERE PID = %s"

        logging.debug("Executing UPDATE query for PARTNER")
        cursor.execute(update_query, update_values)
        connection.commit()

        if cursor.rowcount == 0:
            logging.error("Partner not found or no changes made")
            return jsonify({"error": "Partner not found or no changes made"}), 404

        logging.debug("Partner updated successfully")
        return jsonify({"message": "Partner updated successfully"}), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.debug("Database connection closed")