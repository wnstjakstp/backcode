"""
파트너가 작성한 공고문을 수정하는 api 
본인이 작성한 정보에서 pinfo 테이블의 모든 정보 수정 가능
ATIME에서 0과 1로 평일 주말 시간대 설정 업데이트 가능 0이 아마 평일 
CLOSED에서 0과 1로 휴무일 업데이트 가능 (1이 휴무일)
"""

from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

partner_myinfo_update_bp = Blueprint('partner_myinfo_update', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_myinfo_update_bp.route('/api/partner/myinfo_update', methods=['POST'])
def update():
    data = request.json

    required_fields = ['intro', 'eprice', 'price', 'expert1', 'expert2', 'gname', 'start_time_weekday', 'end_time_weekday', 'start_time_weekend', 'end_time_weekend', 'closed_days']
    for field in required_fields:
        if field not in data:
            logging.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required field: {field}"}), 400

    pid = session.get('partner_id')
    if not pid:
        logging.error("No partner ID in session")
        return jsonify({"error": "No partner ID in session"}), 401

    intro = data['intro']
    eprice = data['eprice']
    price = data['price']
    expert1 = data['expert1']
    expert2 = data['expert2']
    gname = data['gname']
    start_time_weekday = data['start_time_weekday']
    end_time_weekday = data['end_time_weekday']
    start_time_weekend = data['start_time_weekend']
    end_time_weekend = data['end_time_weekend']
    closed_days = data['closed_days']
    ig = data.get('ig', None)
    img = data.get('img', None)

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Update PINFO table
        logging.debug("Updating PINFO table")
        query = """UPDATE PINFO SET INTRO = %s, IG = %s, EXPERT1 = %s, EXPERT2 = %s, PRICE = %s, EPRICE = %s, IMG = %s, GNAME = %s WHERE PID = %s"""
        values = (intro, ig, expert1, expert2, price, eprice, img, gname, pid)
        cursor.execute(query, values)

        # Update ATIME table
        logging.debug("Updating ATIME table")
        weekday_time_query = """UPDATE ATIME SET STARTTIME = %s, ENDTIME = %s WHERE PID = %s AND DAYTYPE = 0"""
        cursor.execute(weekday_time_query, (start_time_weekday, end_time_weekday, pid))

        weekend_time_query = """UPDATE ATIME SET STARTTIME = %s, ENDTIME = %s WHERE PID = %s AND DAYTYPE = 1"""
        cursor.execute(weekend_time_query, (start_time_weekend, end_time_weekend, pid))

        # Update CLOSED table
        logging.debug("Updating CLOSED table")
        closed_query = """UPDATE CLOSED SET MON = %s, TUE = %s, WED = %s, THUR = %s, FRI = %s, SAT = %s, SUN = %s WHERE PID = %s"""
        closed_values = (
            closed_days['mon'],
            closed_days['tue'],
            closed_days['wed'],
            closed_days['thur'],
            closed_days['fri'],
            closed_days['sat'],
            closed_days['sun'],
            pid
        )
        cursor.execute(closed_query, closed_values)
        
        connection.commit()

        logging.debug("Partner information updated successfully")

        # Fetch updated partner details to include in response
        partner_info_query = """
        SELECT p.PID, p.INTRO, p.IG, p.EXPERT1, p.EXPERT2, p.PRICE, p.EPRICE, p.IMG, p.GNAME, 
               pt.NAME as partner_name, pt.GU as partner_gu, pt.DONG as partner_dong, pt.GENDER as partner_gender,
               (SELECT STARTTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 0) as weekday_start_time,
               (SELECT ENDTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 0) as weekday_end_time,
               (SELECT STARTTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 1) as weekend_start_time,
               (SELECT ENDTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 1) as weekend_end_time,
               c.MON, c.TUE, c.WED, c.THUR, c.FRI, c.SAT, c.SUN
        FROM PINFO p
        JOIN PARTNER pt ON p.PID = pt.PID
        JOIN CLOSED c ON p.PID = c.PID
        WHERE p.PID = %s
        """
        cursor.execute(partner_info_query, (pid,))
        partner_info = cursor.fetchone()

        # Create closed days dictionary
        closed_days_dict = {
            "mon": partner_info["MON"],
            "tue": partner_info["TUE"],
            "wed": partner_info["WED"],
            "thur": partner_info["THUR"],
            "fri": partner_info["FRI"],
            "sat": partner_info["SAT"],
            "sun": partner_info["SUN"]
        }

        # Create a dictionary from the partner info tuple
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
            "message": "Partner information updated successfully",
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