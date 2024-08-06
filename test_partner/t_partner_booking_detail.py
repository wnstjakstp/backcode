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

# 예약 상세 정보 조회
booking_detail_url = f"{BASE_URL}/api/booking_detail"
booking_detail_params = {
    "book_id": "5"
}
partner_booking_detail_response = partner_session.get(booking_detail_url, params=booking_detail_params)
if partner_booking_detail_response.status_code == 200:
    print("Partner Booking detail retrieved successfully")
    print("Partner Booking Detail Response:", json.dumps(partner_booking_detail_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve booking detail. Status code: {partner_booking_detail_response.status_code}, Response text: {partner_booking_detail_response.text}")