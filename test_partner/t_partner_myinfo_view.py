import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 파트너 로그인
partner_login_url = f"{BASE_URL}/api/partner/login"
partner_login_data = {
    "pid": "partner1",
    "pw": "password1"
}

session = requests.Session()
partner_login_response = session.post(partner_login_url, json=partner_login_data)
if partner_login_response.status_code == 200:
    print("Partner login successful")
    print("Partner Login Response:", partner_login_response.json())
else:
    print(f"Failed to log in. Status code: {partner_login_response.status_code}, Response text: {partner_login_response.text}")
    exit()

# 파트너 공고문 조회
view_myinfo_url = f"{BASE_URL}/api/partner/myinfo_view"
view_myinfo_response = session.get(view_myinfo_url)
if view_myinfo_response.status_code == 200:
    print("Partner myinfo retrieved successfully")
    print("Partner Myinfo Response:", json.dumps(view_myinfo_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve partner myinfo. Status code: {view_myinfo_response.status_code}, Response text: {view_myinfo_response.text}")