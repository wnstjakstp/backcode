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

# 예약 상세 정보 조회
reservation_detail_url = f"{BASE_URL}/api/reservation_detail"
reservation_detail_params = {
    "rid": "6"  # 실제 예약 ID로 변경
}
reservation_detail_response = session.get(reservation_detail_url, params=reservation_detail_params)
if reservation_detail_response.status_code == 200:
    print("Reservation detail retrieved successfully")
    print("Reservation Detail Response:", json.dumps(reservation_detail_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve reservation detail. Status code: {reservation_detail_response.status_code}, Response text: {reservation_detail_response.text}")