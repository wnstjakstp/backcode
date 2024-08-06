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

# 유저 정기 구독 신청
reservation_url = f"{BASE_URL}/api/reservation/register"
reservation_data = {
    "pid": "partner5",
    "fcount": 10,
    "fdate": "2024-08-03"
}

reservation_response = session.post(reservation_url, json=reservation_data)
if reservation_response.status_code == 201:
    print("Reservation registered successfully")
    print("Reservation Response:", json.dumps(reservation_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to register reservation. Status code: {reservation_response.status_code}, Response text: {reservation_response.text}")