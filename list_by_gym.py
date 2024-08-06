# list_by_gym.py
# 검색한 헬스장 이름으로 pinfo에 일치하는 헬스장 이름찾아서 해당하는 파트너 리스트 반환 
from flask import Blueprint, request, jsonify
import logging
from db_util import create_db_connection

list_by_gym_bp = Blueprint('list_by_gym', __name__)
logging.basicConfig(level=logging.DEBUG)

@list_by_gym_bp.route('/api/gym/partners', methods=['GET'])
def search_gym():
    name = request.args.get('name')
    gu = request.args.get('gu')
    dong = request.args.get('dong')

    query_conditions = []
    query_values = []

    if name:
        query_conditions.append("g.NAME LIKE %s")
        query_values.append(f"%{name}%")
    if gu and not dong:
        query_conditions.append("g.GU = %s")
        query_values.append(gu)
    elif gu and dong:
        query_conditions.append("g.GU = %s AND g.DONG LIKE %s")
        query_values.append(gu)
        query_values.append(f"%{dong}%")
    elif dong and not gu:
        query_conditions.append("g.DONG LIKE %s")
        query_values.append(f"%{dong}%")

    if not query_conditions:
        return jsonify({"error": "At least one search parameter is required"}), 400

    query = f"""
    SELECT g.*, p.PID, pt.NAME as trainer_name, p.INTRO as trainer_intro, p.PRICE as price, p.EPRICE as eprice,
           COALESCE(AVG(r.RATE), 0) AS avg_rate, COUNT(r.REID) AS review_count,
           p.EXPERT1 as expert1, p.EXPERT2 as expert2, p.IMG as trainer_img
    FROM GYM g
    LEFT JOIN PINFO p ON g.NAME = p.GNAME
    LEFT JOIN PARTNER pt ON p.PID = pt.PID
    LEFT JOIN REVIEW r ON p.PID = r.PID
    WHERE {' AND '.join(query_conditions)}
    GROUP BY g.NAME, p.PID, pt.NAME, p.INTRO, p.PRICE, p.EPRICE, p.EXPERT1, p.EXPERT2, p.IMG, g.ADDRESS, g.DONG, g.GU, g.STREET, g.TEL
    ORDER BY g.NAME, pt.NAME
    """

    logging.debug(f"Executing query: {query}")
    logging.debug(f"With values: {query_values}")

    connection = create_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, query_values)
        results = cursor.fetchall()
        
        logging.debug(f"Query results: {results}")

        gyms = {}
        for row in results:
            gym_name = row['NAME']
            if gym_name not in gyms:
                gyms[gym_name] = {
                    'ADDRESS': row['ADDRESS'],
                    'DONG': row['DONG'],
                    'GU': row['GU'],
                    'NAME': row['NAME'],
                    'STREET': row['STREET'],
                    'TEL': row['TEL'],
                    'partners': []
                }
            
            if row['trainer_name']:
                partner_info = {
                    'PID': row['PID'],
                    'trainer_name': row['trainer_name'],
                    'trainer_intro': row['trainer_intro'],
                    'price': row['price'],
                    'eprice': row['eprice'],
                    'avg_rate': row['avg_rate'],
                    'review_count': row['review_count'],
                    'expert1': row['expert1'],
                    'expert2': row['expert2'],
                    'trainer_img': row['trainer_img']
                }
                gyms[gym_name]['partners'].append(partner_info)

        return jsonify(list(gyms.values())), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()