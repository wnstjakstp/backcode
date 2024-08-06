"""
파트너가 본인의 공고문을 조회하는 api
만약 공고문을 작성하지 않았으면 빈 리스트를 반환 
작성하였다면 작성한 정보를 보여줌 
반환되는 값은 피그마 페이지 그대로 해당하는 정보들을 전부 반환함 
***빡셈***
"""

from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

partner_myinfo_view_bp = Blueprint('partner_myinfo_view', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_myinfo_view_bp.route('/api/partner/myinfo_view', methods=['GET'])
def view_myinfo():
    pid = session.get('partner_id')
    if not pid:
        logging.error("No partner ID in session")
        return jsonify({"error": "No partner ID in session"}), 401

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch partner details
        partner_info_query = """
        SELECT p.PID, p.INTRO, p.IG, p.EXPERT1, p.EXPERT2, p.PRICE, p.EPRICE, p.IMG, p.GNAME, 
               pt.NAME as partner_name, pt.GU as partner_gu, pt.DONG as partner_dong, pt.GENDER as partner_gender,
               (SELECT STARTTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 0) as weekday_start_time,
               (SELECT ENDTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 0) as weekday_end_time,
               (SELECT STARTTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 1) as weekend_start_time,
               (SELECT ENDTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 1) as weekend_end_time
        FROM PINFO p
        JOIN PARTNER pt ON p.PID = pt.PID
        WHERE p.PID = %s
        """
        cursor.execute(partner_info_query, (pid,))
        partner_info = cursor.fetchone()

        if not partner_info:
            return jsonify({"partner_info": {}}), 200

        # Fetch closed days
        closed_days_query = "SELECT MON, TUE, WED, THUR, FRI, SAT, SUN FROM CLOSED WHERE PID = %s"
        cursor.execute(closed_days_query, (pid,))
        closed_days_result = cursor.fetchone()
        closed_days_dict = {
            "mon": closed_days_result["MON"],
            "tue": closed_days_result["TUE"],
            "wed": closed_days_result["WED"],
            "thur": closed_days_result["THUR"],
            "fri": closed_days_result["FRI"],
            "sat": closed_days_result["SAT"],
            "sun": closed_days_result["SUN"]
        }

        partner_info_dict = {
            "PID": partner_info["PID"],
            "INTRO": partner_info["INTRO"],
            "IG": partner_info["IG"],
            "EXPERT1": partner_info["EXPERT1"],
            "EXPERT2": partner_info["EXPERT2"],
            "PRICE": partner_info["PRICE"],
            "EPRICE": partner_info["EPRICE"],
            "IMG": partner_info["IMG"],
            "GNAME": partner_info["GNAME"],
            "partner_name": partner_info["partner_name"],
            "partner_gu": partner_info["partner_gu"],
            "partner_dong": partner_info["partner_dong"],
            "partner_gender": partner_info["partner_gender"],
            "weekday_start_time": partner_info["weekday_start_time"],
            "weekday_end_time": partner_info["weekday_end_time"],
            "weekend_start_time": partner_info["weekend_start_time"],
            "weekend_end_time": partner_info["weekend_end_time"],
            "closed_days": closed_days_dict
        }

        response = {
            "message": "Partner application retrieved successfully",
            "partner_info": partner_info_dict
        }

        return jsonify(response), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()