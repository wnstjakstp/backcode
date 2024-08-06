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

# 파트너 예약 리스트 조회
booking_list_url = f"{BASE_URL}/api/partner/booking_list"
booking_list_response = session.post(booking_list_url)
if booking_list_response.status_code == 200:
    print("Booking list retrieved successfully")
    print("Booking List Response:", json.dumps(booking_list_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to retrieve booking list. Status code: {booking_list_response.status_code}, Response text: {booking_list_response.text}")