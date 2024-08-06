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

# 예약 상세 정보 조회
booking_detail_url = f"{BASE_URL}/api/booking_detail"
booking_detail_params = {
    "book_id": "5"
}
booking_detail_response = session.get(booking_detail_url, params=booking_detail_params)
if booking_detail_response.status_code == 200:
    print("Booking detail retrieved successfully")
    print("Booking Detail Response:", json.dumps(booking_detail_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve booking detail. Status code: {booking_detail_response.status_code}, Response text: {booking_detail_response.text}")