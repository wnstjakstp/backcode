import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_search_gym(name, gu=None, dong=None):
    url = f"{BASE_URL}/api/gym/partners"
    params = {
        "name": name
        
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Gyms and partners retrieved successfully")
        gyms = response.json()
        print("Gyms:")
        print(json.dumps(gyms, indent=4, ensure_ascii=False))
    elif response.status_code == 400:
        print("At least one search parameter is required")
    else:
        print(f"Failed to retrieve gyms and partners. Status code: {response.status_code}, Response text: {response.text}")

# 테스트 실행
if __name__ == "__main__":
    test_name = "DYGYM"  # 테스트할 헬스장 이름을 여기에 입력하세요
    test_gu = None  # 테스트할 구를 여기에 입력하세요 (옵션)
    test_dong = None  # 테스트할 동을 여기에 입력하세요 (옵션)
    test_search_gym(test_name, test_gu, test_dong)