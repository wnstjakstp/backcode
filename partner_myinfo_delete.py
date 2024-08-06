"""
파트너가 본인의 공고문을 삭제하는 api 
db에서 삭제됨
"""

from flask import Blueprint, request, jsonify, session
import logging
import mysql.connector
from db_util import create_db_connection

partner_myinfo_delete_bp = Blueprint('partner_myinfo_delete', __name__)
logging.basicConfig(level=logging.DEBUG)

@partner_myinfo_delete_bp.route('/api/partner/myinfo_delete', methods=['DELETE'])
def delete_myinfo():
    pid = session.get('partner_id')
    
    if not pid:
        logging.error("No partner ID in session")
        return jsonify({"error": "No partner ID in session"}), 401

    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        
        # PINFO 테이블 삭제
        delete_pinfo_query = "DELETE FROM PINFO WHERE PID = %s"
        cursor.execute(delete_pinfo_query, (pid,))
        
        # ATIME 테이블 삭제
        delete_atime_query = "DELETE FROM ATIME WHERE PID = %s"
        cursor.execute(delete_atime_query, (pid,))
        
        # CLOSED 테이블 삭제
        delete_closed_query = "DELETE FROM CLOSED WHERE PID = %s"
        cursor.execute(delete_closed_query, (pid,))
        
        connection.commit()

        logging.debug("Partner information deleted successfully")
        return jsonify({"message": "Partner information deleted successfully"}), 200
    except mysql.connector.Error as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()