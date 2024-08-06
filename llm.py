from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일의 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
api_key = os.getenv("OPENAI_API_KEY2")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

# 프롬프트 생성 함수
def create_prompt(user_input):
    messages = [
        {"role": "system", "content": "You are an expert on exercise and diet management. Please answer the questions about exercise and diet management sincerely in three sentences. To any other questions, please reply with '운동과 식단관리에 관한 질문만 답변가능합니다!'. Always answer in Korean."},
        {"role": "user", "content": user_input}
    ]
    return messages

def get_response(user_input):
    # 프롬프트 생성
    messages = create_prompt(user_input)

    try:
        # OpenAI GPT 모델 호출
        response = client.chat.completions.create(
            model="gpt-4",  # 사용하고자 하는 모델명
            messages=messages,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

# 테스트 코드
if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        response = get_response(user_input)
        print(f"DuBot: {response}")