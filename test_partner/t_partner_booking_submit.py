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

# 예약 수락 (시간 변경 없음)
booking_submit_url = f"{BASE_URL}/api/partner/booking_submit"
booking_submit_data = {
    "booking_id": "5"
}

booking_submit_response = partner_session.post(booking_submit_url, json=booking_submit_data)
if booking_submit_response.status_code == 200:
    print("Booking submitted successfully")
    print("Booking Submit Response:", json.dumps(booking_submit_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to submit booking. Status code: {booking_submit_response.status_code}, Response text: {booking_submit_response.text}")

# 예약 수락 (시간 변경 있음)
booking_submit_data_with_time_change = {
    "booking_id": "5",
    "year": "2024",
    "month": "08",
    "day": "15",
    "time": "19:00"
}

booking_submit_response_with_time_change = partner_session.post(booking_submit_url, json=booking_submit_data_with_time_change)
if booking_submit_response_with_time_change.status_code == 200:
    print("Booking with time change submitted successfully")
    print("Booking Submit Response with Time Change:", json.dumps(booking_submit_response_with_time_change.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to submit booking with time change. Status code: {booking_submit_response_with_time_change.status_code}, Response text: {booking_submit_response_with_time_change.text}")