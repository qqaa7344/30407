import streamlit as st
import time

# 1. 페이지 기본 설정 및 스타일
st.set_page_config(page_title="우주 정복 클릭커", page_icon="🚀", layout="centered")

# CSS 스타일링 (피버 타임 전용 불타는 효과 추가)
st.markdown("""
    <style>
    .big-font { font-size:45px !important; font-weight: bold; color: #FF4B4B; text-align: center; }
    .score-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .fever-box { background-color: #FF4B4B; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.8; } }
    </style>
    """, unsafe_allow_html=True)

# 2. 게임 상태(Session State) 초기화
if 'gold' not in st.session_state:
    st.session_state.gold = 0
    st.session_state.click_power = 1
    
    # [피버 타임 관련 변수 추가]
    st.session_state.fever_gauge = 0          # 피버 게이지 (0 ~ 100)
    st.session_state.is_fever = False          # 현재 피버 타임 여부
    st.session_state.fever_end_time = 0        # 피버 타임이 끝나는 시간
    
    # 업그레이드 품목들
    st.session_state.upgrades = {
        'booster': {'name': '🚀 고성능 부스터 (클릭 파워 +1)', 'level': 0, 'cost': 15, 'effect': 1},
        'robot': {'name': '🤖 자동 채굴 로봇 (초당 +1 골드)', 'level': 0, 'cost': 50, 'effect': 1},
        'factory': {'name': '🏭 우주 정거장 공장 (초당 +10 골드)', 'level': 0, 'cost': 400, 'effect': 10},
        'quantum': {'name': '⚛️ 양자 동력원 (초당 +100 골드)', 'level': 0, 'cost': 3000, 'effect': 100}
    }
    
    # 승리 조건 금액 (밸런스를 위해 목표 상향 조정)
    st.session_state.victory_target = 300000
    st.session_state.game_over = False
    st.session_state.last_time = time.time()

# 3. 실시간 피버 타임 시간 체크
current_time = time.time()
if st.session_state.is_fever and current_time > st.session_state.fever_end_time:
    st.session_state.is_fever = False
    st.session_state.fever_gauge = 0

# 4. 실시간 자동 골드 획득 계산
elapsed = current_time - st.session_state.last_time
st.session_state.last_time = current_time

# 초당 기본 자동 생산량(GPS) 계산
base_gps = (st.session_state.upgrades['robot']['level'] * st.session_state.upgrades['robot']['effect'] +
            st.session_state.upgrades['factory']['level'] * st.session_state.upgrades['factory']['effect'] +
            st.session_state.upgrades['quantum']['level'] * st.session_state.upgrades['quantum']['effect'])

# 피버 타임일 때는 모든 생산량과 클릭 파워가 3배!
multiplier = 3 if st.session_state.is_fever else 1
current_gps = base_gps * multiplier
current_click_power = st.session_state.click_power * multiplier

# 흘러간 시간만큼 골드 누적
if not st.session_state.game_over:
    st.session_state.gold += current_gps * elapsed

# 5. 게임 화면 그리기
st.title("🌌 우주 정복 클릭커 (Space Clicker)")
st.caption("목표: 300,000 골드를 모아 우주선을 최종 진화시키고 우주를 정복하세요!")

# 엔딩 화면 조건 검사
if st.session_state.gold >= st.session_state.victory_target:
    st.session_state.game_over = True

if st.session_state.game_over:
    st.balloons()
    st.markdown("<p class='big-font'>🎉 우주 정복 성공! 🎉</p>", unsafe_allow_html=True)
    st.success(f"최종 {int(st.session_state.gold):,} 골드를 모아 은하계 최고의 지배자가 되었습니다!")
    if st.button("게임 다시 시작하기"):
        st.session_state.clear()
        st.rerun()
else:
    # 피버 타임 여부에 따른 UI 변경
    if st.session_state.is_fever:
        remaining_fever = max(0, int(st.session_state.fever_end_time - current_time))
        st.markdown(f"""
            <div class='fever-box'>
                <h2>🔥 FEVER TIME (보상 3배!) 🔥</h2>
                <p style='font-size:20px;'>남은 시간: {remaining_fever}초</p>
                <p class='big-font'>💰 {int(st.session_state.gold):,}</p>
                <p>초당 자동 생산량(GPS): ⚡ {current_gps:,} / 클릭당 파워: 👆 {current_click_power}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='score-box'>
                <h3>현재 보유 골드</h3>
                <p class='big-font'>💰 {int(st.session_state.gold):,}</p>
                <p>초당 자동 생산량(GPS): ⚡ {current_gps:,} / 클릭당 파워: 👆 {current_click_power}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # 진행도 바 (Progress Bar)
    progress = min(st.session_state.gold / st.session_state.victory_target, 1.0)
    st.progress(progress, text=f"우주 정복 진척도: {progress*100:.1f}%")

    # 피버 게이지 출력 (피버 타임이 아닐 때만)
    if not st.session_state.is_fever:
        fever_progress = min(st.session_state.fever_gauge / 100, 1.0)
        st.progress(fever_progress, text=f"🔥 피버 게이지: {st.session_state.fever_gauge}% (100% 시 3배 버프!)")

    # 대형 클릭 버튼
    btn_label = "🔥 피버 클릭!!! 🔥" if st.session_state.is_fever else "🛸 우주선 클릭하기 (골드 획득!)"
    if st.button(btn_label, use_container_width=True):
        st.session_state.gold += current_click_power
        
        # 클릭할 때마다 피버 게이지 상승 (피버 타임이 아닐 때만)
        if not st.session_state.is_fever:
            st.session_state.fever_gauge += 4  # 25번 클릭하면 피버 타임 진입
            if st.session_state.fever_gauge >= 100:
                st.session_state.is_fever = True
                st.session_state.fever_end_time = time.time() + 10  # 10초 동안 지속
        st.rerun()

    st.markdown("---")
    st.subheader("🛒 상점 및 연구소")

    col1, col2 = st.columns(2)

    with col1:
        b_up = st.session_state.upgrades['booster']
        if st.button(f"{b_up['name']}\n\n비용: {b_up['cost']} 💰 (Lv.{b_up['level']})", use_container_width=True):
            if st.session_state.gold >= b_up['cost']:
                st.session_state.gold -= b_up['cost']
                st.session_state.click_power += b_up['effect']
                b_up['level'] += 1
                b_up['cost'] = int(b_up['cost'] * 1.5)
                st.rerun()
            else:
                st.error("골드가 부족합니다!")

        r_up = st.session_state.upgrades['robot']
        if st.button(f"{r_up['name']}\n\n비용: {r_up['cost']} 💰 (Lv.{r_up['level']})", use_container_width=True):
            if st.session_state.gold >= r_up['cost']:
                st.session_state.gold -= r_up['cost']
                r_up['level'] += 1
                r_up['cost'] = int(r_up['cost'] * 1.6)
                st.rerun()
            else:
                st.error("골드가 부족합니다!")

    with col2:
        f_up = st.session_state.upgrades['factory']
        if st.button(f"{f_up['name']}\n\n비용: {f_up['cost']} 💰 (Lv.{f_up['level']})", use_container_width=True):
            if st.session_state.gold >= f_up['cost']:
                st.session_state.gold -= f_up['cost']
                f_up['level'] += 1
                f_up['cost'] = int(f_up['cost'] * 1.7)
                st.rerun()
            else:
                st.error("골드가 부족합니다!")

        q_up = st.session_state.upgrades['quantum']
        if st.button(f"{q_up['name']}\n\n비용: {q_up['cost']} 💰 (Lv.{q_up['level']})", use_container_width=True):
            if st.session_state.gold >= q_up['cost']:
                st.session_state.gold -= q_up['cost']
                q_up['level'] += 1
                q_up['cost'] = int(q_up['cost'] * 1.8)
                st.rerun()
            else:
                st.error("골드가 부족합니다!")

    # 1초마다 화면 갱신
    time.sleep(1.0)
    st.rerun()
