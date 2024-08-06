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

# 유저 예약 취소
cancel_booking_url = f"{BASE_URL}/api/user/booking_cancel"
cancel_booking_data = {
    "booking_id": 7  # 실제 booking_id를 사용해야 합니다.
}

cancel_booking_response = session.post(cancel_booking_url, json=cancel_booking_data)
if cancel_booking_response.status_code == 200:
    print("Booking canceled successfully")
    print("Cancel Booking Response:", cancel_booking_response.json())
else:
    print(f"Failed to cancel booking. Status code: {cancel_booking_response.status_code}, Response text: {cancel_booking_response.text}")