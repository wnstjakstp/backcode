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

# 공고문 작성
write_myinfo_url = f"{BASE_URL}/api/partner/myinfo_write"
write_myinfo_data = {
    "intro": "Experienced personal trainer offering customized workout plans.",
    "eprice": 20000,
    "price": 300000,
    "expert1": "Weight loss",
    "expert2": "Muscle building",
    "gname": "926fit",
    "start_time_weekday": "06:00",
    "end_time_weekday": "22:00",
    "start_time_weekend": "08:00",
    "end_time_weekend": "20:00",
    "closed_days": {
        "mon": 0,
        "tue": 0,
        "wed": 1,
        "thur": 1,
        "fri": 0,
        "sat": 0,
        "sun": 1
    },
    "ig": "@trainer_ig",
    "img": "image_url"
}

write_myinfo_response = session.post(write_myinfo_url, json=write_myinfo_data)
if write_myinfo_response.status_code == 201:
    print("Partner write myinfo successful")
    print("Write Myinfo Response:", json.dumps(write_myinfo_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to write myinfo. Status code: {write_myinfo_response.status_code}, Response text: {write_myinfo_response.text}")