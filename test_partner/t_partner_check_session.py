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

# PT 세션 체크
check_session_url = f"{BASE_URL}/api/partner/check_session"
check_session_data = {
    "rid": "6"  # 실제 예약 ID로 변경
}

check_session_response = session.post(check_session_url, json=check_session_data)
if check_session_response.status_code == 201:
    print("Session checked successfully")
    print("Check Session Response:", json.dumps(check_session_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to check session. Status code: {check_session_response.status_code}, Response text: {check_session_response.text}")