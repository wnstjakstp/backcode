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

# 공고문 정보 수정
update_myinfo_url = f"{BASE_URL}/api/partner/myinfo_update"
update_myinfo_data = {
    "intro": "Updatedasdasdasdasda introduction",
    "eprice": 2500,
    "price": 3000,
    "expert1": "Weight loss",
    "expert2": "Muscle building",
    "gname": "926fit",
    "start_time_weekday": "11:00",
    "end_time_weekday": "11:00",
    "start_time_weekend": "11:00",
    "end_time_weekend": "11:00",
    "closed_days": {
        "mon": 0,
        "tue": 1,
        "wed": 1,
        "thur": 1,
        "fri": 0,
        "sat": 1,
        "sun": 1
    },
    "ig": "updated_instagram_handle",
    "img": "updated_image_url"
}

update_myinfo_response = session.post(update_myinfo_url, json=update_myinfo_data)
if update_myinfo_response.status_code == 200:
    print("Partner information updated successfully")
    print("Update Myinfo Response:", json.dumps(update_myinfo_response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to update partner information. Status code: {update_myinfo_response.status_code}, Response text: {update_myinfo_response.text}")