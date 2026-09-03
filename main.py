import random
import streamlit as st  # 스트림릿 라이브러리 추가

def generate_korean_name(last_name):
    """
    random.choice만 사용하여 두 글자 이름을 조합합니다.
    """
    first_chars = ["민", "서", "하", "준", "예", "도", "시", "우", "지", "유", "연", "수", "윤", "재", "정"]
    second_chars = ["아", "은", "현", "원", "진", "석", "호", "훈", "빈", "율", "영", "성", "욱", "희", "경"]
    
    char1 = random.choice(first_chars)
    char2 = random.choice(second_chars)
    
    return f"{last_name}{char1}{char2}"

# --- 스트림릿 웹 화면 구성 ---

st.title("👤 랜덤 한국어 이름 생성기")
st.write("원하는 성씨를 입력하면 랜덤으로 예쁜 이름을 추천해 드립니다.")

# [수정] input() 대신 st.text_input() 사용
input_last_name = st.text_input("원하는 성씨를 입력하세요 (예: 김, 이, 박)", value="김").strip()

# 이름을 생성하는 버튼 추가
if st.button("이름 생성하기"):
    if input_last_name:
        st.subheader(f"✨ '{input_last_name}'씨를 위한 추천 이름 5개")
        
        # [수정] print() 대신 st.write()나 st.success() 사용
        for _ in range(5):
            name = generate_korean_name(input_last_name)
            st.success(f"👤 {name}")
    else:
        st.warning("성씨를 입력해 주세요!")
