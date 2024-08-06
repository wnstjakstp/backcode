import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 파트너 로그인
partner_login_url = f"{BASE_URL}/api/partner/login"
partner_login_data = {
    "pid": "partner9",
    "pw": "password9"
}

session = requests.Session()
partner_login_response = session.post(partner_login_url, json=partner_login_data)
if partner_login_response.status_code == 200:
    print("Partner login successful")
    print("Partner Login Response:", partner_login_response.json())
else:
    print(f"Failed to log in. Status code: {partner_login_response.status_code}, Response text: {partner_login_response.text}")
    exit()

# 공고문 삭제
delete_myinfo_url = f"{BASE_URL}/api/partner/myinfo_delete"
delete_myinfo_response = session.delete(delete_myinfo_url)
if delete_myinfo_response.status_code == 200:
    print("Partner delete myinfo successful")
    print("Delete Myinfo Response:", json.dumps(delete_myinfo_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to delete myinfo. Status code: {delete_myinfo_response.status_code}, Response text: {delete_myinfo_response.text}")