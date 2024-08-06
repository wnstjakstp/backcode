import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 유저 로그인
user_login_url = f"{BASE_URL}/api/user/login"
user_login_data = {
    "uid": "user2",
    "pw": "password2"
}

session = requests.Session()
user_login_response = session.post(user_login_url, json=user_login_data)
if user_login_response.status_code == 200:
    print("User login successful")
    print("User Login Response:", user_login_response.json())
else:
    print(f"Failed to log in. Status code: {user_login_response.status_code}, Response text: {user_login_response.text}")
    exit()

# 구독 취소
cancel_reservation_url = f"{BASE_URL}/api/user/cancel_reservation"
cancel_reservation_data = {
    "rid": 3  # 실제 삭제하려는 Reservation ID를 여기에 넣으세요
}
cancel_reservation_response = session.post(cancel_reservation_url, json=cancel_reservation_data)
if cancel_reservation_response.status_code == 200:
    print("Reservation canceled successfully")
    print("Cancel Reservation Response:", cancel_reservation_response.json())
else:
    print(f"Failed to cancel reservation. Status code: {cancel_reservation_response.status_code}, Response text: {cancel_reservation_response.text}")