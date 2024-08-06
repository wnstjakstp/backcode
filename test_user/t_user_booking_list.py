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

# 유저 예약 목록 조회
booking_list_url = f"{BASE_URL}/api/user/booking_list"
booking_list_response = session.get(booking_list_url)
if booking_list_response.status_code == 200:
    print("Booking list retrieved successfully")
    print("Booking List Response:", json.dumps(booking_list_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve booking list. Status code: {booking_list_response.status_code}, Response text: {booking_list_response.text}")