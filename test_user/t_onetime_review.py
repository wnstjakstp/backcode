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

# 1회 체험 후기 작성
one_time_review_url = f"{BASE_URL}/api/review/one_time"
one_time_review_data = {
    "pid": "partner1",
    "rate": 5,
    "content": "Great experience!"
}

one_time_review_response = session.post(one_time_review_url, json=one_time_review_data)
if one_time_review_response.status_code == 201:
    print("One-time review added successfully")
    print("One-time Review Response:", one_time_review_response.json())
else:
    print(f"Failed to add one-time review. Status code: {one_time_review_response.status_code}, Response text: {one_time_review_response.text}")