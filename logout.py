# 로그아웃 api

from flask import Blueprint, session, jsonify
import logging

logout_bp = Blueprint('logout', __name__)
logging.basicConfig(level=logging.DEBUG)

@logout_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    logging.debug("User logged out successfully")
    return jsonify({"message": "Logged out successfully"}), 200