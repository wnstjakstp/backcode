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

# 예약 등록
booking_register_url = f"{BASE_URL}/api/booking/register"
booking_register_data = {
    "pid": "partner2",
    "year": 2024,
    "month": 8,
    "day": 15,
    "time": "10:00",
    "purpose": "Weight loss",
    "experience": "Beginner",
    "preferred_time": "Morning"
}

booking_register_response = session.post(booking_register_url, json=booking_register_data)
if booking_register_response.status_code == 201:
    print("Booking registered successfully")
    print("Booking Register Response:", json.dumps(booking_register_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to register booking. Status code: {booking_register_response.status_code}, Response text: {booking_register_response.text}")