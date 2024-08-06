from flask import Flask, request, jsonify, Blueprint
import logging
from llm import get_response

# Flask 애플리케이션 생성
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# 블루프린트 생성
dubot_bp = Blueprint('dubot', __name__)

@dubot_bp.route('/api/dubot', methods=['POST'])
def dubot():
    data = request.json
    user_input = data.get("user_input")
    
    if not user_input:
        return jsonify({"error": "No user input provided"}), 400
    
    response = get_response(user_input)
    return jsonify({"user_input": user_input, "response": response})

# 블루프린트 등록
app.register_blueprint(dubot_bp)

if __name__ == "__main__":
    app.run(debug=True)