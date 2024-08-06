from flask import Flask
from dotenv import load_dotenv
import os
from db_util import create_db_connection  # 추가된 부분
from dubot import dubot_bp
# .env 파일 로드
load_dotenv()

# 환경 변수
secret_key = os.getenv('SECRET_KEY', 'supersecretkey')

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = secret_key

# 블루프린트 등록
from partner_register import partner_register_bp # 파트너 회원가입
from user_register import user_register_bp # 유저 회원가입
from partner_login import partner_login_bp # 파트너 로그인
from user_login import user_login_bp # 유저 로그인
from logout import logout_bp # 유저, 파트너 로그아웃 
from partner_update import partner_update_bp # 파트너 정보 수정
from user_update import user_update_bp # 유저 정보 수정 

from gym_search import gym_search_bp # 구, 동으로 선택 / 이름으로 헬스장 검색 
from user_home import user_home_bp # 유저 홈 진입 파트너 리스트 
from list_by_gym import list_by_gym_bp # 헬스장 기준으로 파트너 리스트 조회 

from partner_myinfo_view import partner_myinfo_view_bp # 파트너가 공고문 상세정보 조회 
from partner_myinfo_write import partner_myinfo_write_bp # 파트너가 공고문 작성
from partner_myinfo_update import partner_myinfo_update_bp # 파트너 공고문 수정
from partner_myinfo_delete import partner_myinfo_delete_bp # 파트너 공고문 삭제 

from user_view_partnerinfo import user_view_partnerinfo_bp # 유저가 파트너 공고문 상세정보 
from user_view_partner_reviews import user_view_partner_reviews_bp
from booking import booking_bp # 유저가 1회 예약 신청 


from booking_detail import booking_detail_bp # 유저와 파트너가 예약 상세정보 봄 
from partner_booking_cancel import partner_booking_cancel_bp # 파트너가 예약 거절

from partner_booking_submit import partner_booking_submit_bp # 파트너가 예약 수락 
from partner_booking_list import partner_booking_list_bp # 파트너 예약 리스트 호출
from user_booking_list import user_booking_list_bp # 유저의 예약 리스트 호출 

from reservation import reservation_bp # 유저 정기 예약 신청 

from reservation_detail import reservation_detail_bp # 정기 예약 상세 
from partner_r_list import partner_r_list_bp # 파트너 구독 리스트 
from user_r_list import user_r_list_bp # 유저 구독 리스트  
from partner_check_session import partner_check_session_bp # 횟수 체크 
from user_r_cancel import user_r_cancel_bp # 유저 구독 취소 
from user_booking_cancel import user_booking_cancel_bp  # 올바르게 가져오기

from onetime_review import onetime_review_bp
from subscription_review import subscription_review_bp

from dubot import dubot_bp

#######################순서 흐름 app.register로 볼 것#################################################
# 파트너 유저 회원가입 #
app.register_blueprint(partner_register_bp) # 파트너 회원가입o
app.register_blueprint(user_register_bp) # 유저 회원가입o
app.register_blueprint(partner_login_bp) # 파트너 로그인o
app.register_blueprint(user_login_bp) # 유저 로그인o
app.register_blueprint(logout_bp) # 로그아웃 (파트너,유저)o

# 개인정보 수정 # 
app.register_blueprint(partner_update_bp) # 파트너 개인 정보 수정-
app.register_blueprint(user_update_bp) # 유저 개인 정보 수정 -

# 홈 
app.register_blueprint(gym_search_bp) # 헬스장 검색 (구, 동, 헬스장 이름)o
app.register_blueprint(list_by_gym_bp) # 선택한 헬스장 기준으로 파트너 리스트 반환 o
app.register_blueprint(user_home_bp) # 유저 동 기준으로 파트너 리스트 반환o

# 파트너 공고문 관련 # 
app.register_blueprint(partner_myinfo_view_bp) # 파트너 공고문 조회o
app.register_blueprint(partner_myinfo_write_bp) # 파트너 공고문 작성o
app.register_blueprint(partner_myinfo_update_bp) # 파트너 공고문 수정o
app.register_blueprint(partner_myinfo_delete_bp) # 파트너 공고문 삭제o

# 유저 파트너 공고문 조회 # 
app.register_blueprint(user_view_partnerinfo_bp) # 파트너 공고문 조회o
app.register_blueprint(user_view_partner_reviews_bp) # 파트너의 리뷰 조회o

# 예약 신청 # 
# 유저
app.register_blueprint(booking_bp) # 유저가 예약을 신청o
app.register_blueprint(user_booking_list_bp) # 유저 신청 내역 리스트 o
app.register_blueprint(user_booking_cancel_bp) # 유저 예약 신청 취소 o
# 파트너
app.register_blueprint(partner_booking_list_bp) # 파트너 예약내역 리스트o
app.register_blueprint(partner_booking_cancel_bp) # 파트너 예약내역 취소o
app.register_blueprint(partner_booking_submit_bp) # 파트너 예약내역 수락o
# 공유
app.register_blueprint(booking_detail_bp) # 예약 내역 상세정보 (파트너, 유저)o

# 정기 구독#---------------------------------------------------
# 유저
app.register_blueprint(reservation_bp) # 유저 정기 구독 신청 세모
app.register_blueprint(user_r_list_bp) # 유저 정기 구독 내역 리스트 o
app.register_blueprint(user_r_cancel_bp) # 유저 정기 구독 취소 o

# 파트너
app.register_blueprint(partner_r_list_bp) # 파트너 정기 구독 리스트 o
app.register_blueprint(partner_check_session_bp) # 파트너 횟수 체크 o 

# 공유
app.register_blueprint(reservation_detail_bp) # 정기 구독 상세정보 (파트너, 유저) o

# 후기 작성 관련 # 
app.register_blueprint(onetime_review_bp) # 1회 체험 후기 작성o
app.register_blueprint(subscription_review_bp) # 정기 구독 후기 작성o

# 듀봇 #
app.register_blueprint(dubot_bp)# o



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)