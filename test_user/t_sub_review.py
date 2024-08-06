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

# 정기 구독 후기 작성
subscription_review_url = f"{BASE_URL}/api/review/subscription"
subscription_review_data = {
    "pid": "partner1",
    "rate": 3,
    "content": "Excellent ongoing training!"
}

subscription_review_response = session.post(subscription_review_url, json=subscription_review_data)
if subscription_review_response.status_code == 201:
    print("Subscription review added successfully")
    print("Subscription Review Response:", json.dumps(subscription_review_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to add subscription review. Status code: {subscription_review_response.status_code}, Response text: {subscription_review_response.text}")