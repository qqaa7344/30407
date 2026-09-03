import random

def generate_korean_name(last_name):
    """
    random.choice만 사용하여 두 글자 이름을 조합합니다.
    """
    # 1번째 글자와 2번째 글자의 후보를 겹치지 않게 나누어 구성 (중복 원천 차단)
    first_chars = ["민", "서", "하", "준", "예", "도", "시", "우", "지", "유", "연", "수", "윤", "재", "정"]
    second_chars = ["아", "은", "현", "원", "진", "석", "호", "훈", "빈", "율", "영", "성", "욱", "희", "경"]
    
    # 각 리스트에서 무작위로 1글자씩 선택
    char1 = random.choice(first_chars)
    char2 = random.choice(second_chars)
    
    return f"{last_name}{char1}{char2}"

# --- 사용 예시 ---

# 입력받을 때 공백을 미리 제거합니다.
input_last_name = input("원하는 성씨를 입력하세요 (예: 김, 이, 박): ").strip()

print(f"\n✨ '{input_last_name}'씨를 위한 추천 이름 5개:")
print("-" * 30)

for _ in range(5):
    print(f"👤 {generate_korean_name(input_last_name)}")
