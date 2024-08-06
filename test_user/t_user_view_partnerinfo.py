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

# 파트너 상세 정보 조회 (후기 포함)
partner_detail_url = f"{BASE_URL}/api/user/partner_detail"
partner_detail_params = {"partner_id": "partner2"}
partner_detail_response = session.get(partner_detail_url, params=partner_detail_params)
if partner_detail_response.status_code == 200:
    print("Partner detail retrieved successfully")
    print("Partner Detail Response:", json.dumps(partner_detail_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve partner detail. Status code: {partner_detail_response.status_code}, Response text: {partner_detail_response.text}")