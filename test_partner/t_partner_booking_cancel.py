import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 파트너 로그인
partner_login_url = f"{BASE_URL}/api/partner/login"
partner_login_data = {
    "pid": "partner2",
    "pw": "password2"
}

partner_session = requests.Session()
partner_login_response = partner_session.post(partner_login_url, json=partner_login_data)
if partner_login_response.status_code == 200:
    print("Partner login successful")
    print("Partner Login Response:", partner_login_response.json())
else:
    print(f"Failed to log in. Status code: {partner_login_response.status_code}, Response text: {partner_login_response.text}")
    exit()

# 예약 거절 (삭제)
booking_cancel_url = f"{BASE_URL}/api/partner/booking_cancel"
booking_cancel_data = {
    "booking_id": "2"
}

booking_cancel_response = partner_session.post(booking_cancel_url, json=booking_cancel_data)
if booking_cancel_response.status_code == 200:
    print("Booking canceled successfully")
    print("Booking Cancel Response:", json.dumps(booking_cancel_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to cancel booking. Status code: {booking_cancel_response.status_code}, Response text: {booking_cancel_response.text}")