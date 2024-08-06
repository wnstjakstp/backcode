from flask import Blueprint, request, jsonify
import logging
import mysql.connector
from db_util import create_db_connection

user_view_partnerinfo_bp = Blueprint('user_view_partnerinfo', __name__)
logging.basicConfig(level=logging.DEBUG)

@user_view_partnerinfo_bp.route('/api/user/partner_detail', methods=['GET'])
def detail():
    partner_id = request.args.get('partner_id')
    
    if not partner_id:
        logging.error("No partner ID provided")
        return jsonify({"error": "No partner ID provided"}), 400

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch partner details
        logging.debug("Fetching partner details")
        partner_info_query = """
        SELECT p.PID, p.INTRO, p.IG, p.EXPERT1, p.EXPERT2, p.PRICE, p.EPRICE, p.IMG, p.GNAME, 
               pt.NAME as partner_name, pt.GU as partner_gu, pt.DONG as partner_dong, pt.GENDER as partner_gender,
               (SELECT STARTTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 0) as weekday_start_time,
               (SELECT ENDTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 0) as weekday_end_time,
               (SELECT STARTTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 1) as weekend_start_time,
               (SELECT ENDTIME FROM ATIME WHERE PID = p.PID AND DAYTYPE = 1) as weekend_end_time,
               c.MON, c.TUE, c.WED, c.THUR, c.FRI, c.SAT, c.SUN,
               COALESCE(AVG(r.RATE), 0) AS avg_rate, COUNT(r.REID) AS review_count,
               g.ADDRESS as gym_address
        FROM PINFO p
        JOIN PARTNER pt ON p.PID = pt.PID
        JOIN CLOSED c ON p.PID = c.PID
        LEFT JOIN REVIEW r ON p.PID = r.PID
        JOIN GYM g ON p.GNAME = g.NAME
        WHERE p.PID = %s
        GROUP BY p.PID, pt.NAME, c.MON, c.TUE, c.WED, c.THUR, c.FRI, c.SAT, c.SUN, g.ADDRESS
        """
        cursor.execute(partner_info_query, (partner_id,))
        partner_info = cursor.fetchone()

        if not partner_info:
            logging.error("Partner not found")
            return jsonify({"error": "Partner not found"}), 404

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
            "closed_days": closed_days_dict,
            "avg_rate": partner_info["avg_rate"],
            "review_count": partner_info["review_count"],
            "gym_address": partner_info["gym_address"]
        }

        response = {
            "message": "Partner information retrieved successfully",
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