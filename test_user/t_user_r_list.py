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

# 유저 정기 구독 내역 조회
user_r_list_url = f"{BASE_URL}/api/user/r_list"

user_r_list_response = session.get(user_r_list_url)
if user_r_list_response.status_code == 200:
    print("Reservation list retrieved successfully")
    print("Reservation List Response:", json.dumps(user_r_list_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve reservation list. Status code: {user_r_list_response.status_code}, Response text: {user_r_list_response.text}")