import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 파트너 로그인
partner_login_url = f"{BASE_URL}/api/partner/login"
partner_login_data = {
    "pid": "partner1",
    "pw": "password1"
}

partner_session = requests.Session()
partner_login_response = partner_session.post(partner_login_url, json=partner_login_data)
if partner_login_response.status_code == 200:
    print("Partner login successful")
    print("Partner Login Response:", partner_login_response.json())
else:
    print(f"Failed to log in. Status code: {partner_login_response.status_code}, Response text: {partner_login_response.text}")
    exit()

# 구독 리스트 조회
subscription_list_url = f"{BASE_URL}/api/partner/r_list"
subscription_list_response = partner_session.get(subscription_list_url)
if subscription_list_response.status_code == 200:
    print("Subscription list retrieved successfully")
    print("Subscription List Response:", json.dumps(subscription_list_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve subscription list. Status code: {subscription_list_response.status_code}, Response text: {subscription_list_response.text}")