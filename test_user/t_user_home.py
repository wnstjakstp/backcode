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

# 유저 홈 화면 - 파트너 리스트 조회
user_home_url = f"{BASE_URL}/api/user/home"
user_home_data = {"uid": "user1"}
user_home_response = session.post(user_home_url, json=user_home_data)
if user_home_response.status_code == 200:
    print("User home - Partner list retrieved successfully")
    partners = user_home_response.json()
    print("Partner List Response:", json.dumps(partners, indent=4))
else:
    print(f"Failed to retrieve partner list. Status code: {user_home_response.status_code}, Response text: {user_home_response.text}")