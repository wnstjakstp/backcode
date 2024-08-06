# 구, 동 구와 동, 헬스장 이름으로 헬스장 검색 
from flask import Blueprint, request, jsonify
import logging
from db_util import create_db_connection

gym_search_bp = Blueprint('gym_search', __name__)
logging.basicConfig(level=logging.DEBUG)

@gym_search_bp.route('/api/gym/search', methods=['GET'])
def search_gym():
    name = request.args.get('name')
    gu = request.args.get('gu')
    dong = request.args.get('dong')

    query_conditions = []
    query_values = []

    if name:
        query_conditions.append("NAME LIKE %s")
        query_values.append(f"%{name}%")
    if gu and not dong:
        query_conditions.append("GU = %s")
        query_values.append(gu)
    elif gu and dong:
        query_conditions.append("GU = %s AND DONG LIKE %s")
        query_values.append(gu)
        query_values.append(f"%{dong}%")
    elif dong and not gu:
        query_conditions.append("DONG LIKE %s")
        query_values.append(f"%{dong}%")

    if not query_conditions:
        return jsonify({"error": "At least one search parameter is required"}), 400

    query = f"SELECT * FROM GYM WHERE {' AND '.join(query_conditions)}"

    connection = create_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, query_values)
        gyms = cursor.fetchall()
        if not gyms:
            return jsonify({"message": "No gyms found for the given criteria"}), 404
        return jsonify(gyms), 200
    except Error as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()