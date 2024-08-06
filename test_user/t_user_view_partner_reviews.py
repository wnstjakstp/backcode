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

# 파트너 리뷰 조회
partner_reviews_url = f"{BASE_URL}/api/user/partner_reviews"
partner_reviews_params = {"partner_id": "partner1"}
partner_reviews_response = session.get(partner_reviews_url, params=partner_reviews_params)
if partner_reviews_response.status_code == 200:
    print("Partner reviews retrieved successfully")
    print("Partner Reviews Response:", json.dumps(partner_reviews_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve partner reviews. Status code: {partner_reviews_response.status_code}, Response text: {partner_reviews_response.text}")