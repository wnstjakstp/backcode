import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 유저 로그인
user_login_url = f"{BASE_URL}/api/user/login"
user_login_data = {
    "uid": "user1",
    "pw": "password1"
}

session = requests.Session()
user_login_response = session.post(user_login_url, json=user_login_data)
if user_login_response.status_code == 200:
    print("User login successful")
    print("User Login Response:", user_login_response.json())
else:
    print(f"Failed to log in. Status code: {user_login_response.status_code}, Response text: {user_login_response.text}")
    exit()

# 구독 상세 정보 조회
reservation_detail_url = f"{BASE_URL}/api/reservation_detail"
reservation_detail_params = {
    "rid": "6"
}
reservation_detail_response = session.get(reservation_detail_url, params=reservation_detail_params)
if reservation_detail_response.status_code == 200:
    print("Reservation detail retrieved successfully")
    print("Reservation Detail Response:", json.dumps(reservation_detail_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve reservation detail. Status code: {reservation_detail_response.status_code}, Response text: {reservation_detail_response.text}")