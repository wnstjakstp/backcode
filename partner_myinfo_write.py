"""
파트너가 본인 공고문 작성 api 
다 작성하면 PINFO ATIME CLOSED 에 저장되고 프론트에서 필요한 값 반환
"""
from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

partner_myinfo_write_bp = Blueprint('partner_myinfo_write', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_myinfo_write_bp.route('/api/partner/myinfo_write', methods=['POST'])
def apply():
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

        # Check if the partner already has an application
        logging.debug("Checking for existing application")
        check_query = "SELECT COUNT(*) FROM PINFO WHERE PID = %s"
        cursor.execute(check_query, (pid,))
        result = cursor.fetchone()
        if result['COUNT(*)'] > 0:
            logging.error("Partner already has an application")
            return jsonify({"error": "Partner already has an application"}), 400

        # Check if the gym exists
        logging.debug("Executing SELECT query for GYM")
        gym_query = "SELECT * FROM GYM WHERE NAME = %s"
        cursor.execute(gym_query, (gname,))
        gym = cursor.fetchone()

        if not gym:
            logging.error("Gym not found")
            return jsonify({"error": "Gym not found"}), 404

        # Insert into PINFO table
        logging.debug("Executing INSERT query for PINFO")
        query = """INSERT INTO PINFO (PID, INTRO, IG, EXPERT1, EXPERT2, PRICE, EPRICE, IMG, GNAME) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (pid, intro, ig, expert1, expert2, price, eprice, img, gname)
        cursor.execute(query, values)

        # Insert into ATIME table
        logging.debug("Inserting weekday available time")
        weekday_time_query = """INSERT INTO ATIME (PID, DAYTYPE, STARTTIME, ENDTIME) 
                                VALUES (%s, %s, %s, %s)"""
        cursor.execute(weekday_time_query, (pid, 0, start_time_weekday, end_time_weekday))

        logging.debug("Inserting weekend available time")
        weekend_time_query = """INSERT INTO ATIME (PID, DAYTYPE, STARTTIME, ENDTIME) 
                                VALUES (%s, %s, %s, %s)"""
        cursor.execute(weekend_time_query, (pid, 1, start_time_weekend, end_time_weekend))

        # Insert into CLOSED table
        logging.debug("Inserting closed days")
        closed_query = """INSERT INTO CLOSED (PID, MON, TUE, WED, THUR, FRI, SAT, SUN) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        closed_values = (
            pid,
            closed_days['mon'],
            closed_days['tue'],
            closed_days['wed'],
            closed_days['thur'],
            closed_days['fri'],
            closed_days['sat'],
            closed_days['sun']
        )
        cursor.execute(closed_query, closed_values)
        
        connection.commit()

        logging.debug("Partner application submitted successfully")

        # Fetch partner details to include in response
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
            "message": "Partner application submitted successfully",
            "partner_info": partner_info_dict
        }

        return jsonify(response), 201
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()