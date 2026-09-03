import streamlit as st
import time
import random
from streamlit_autorefresh import st_autorefresh

# 웹페이지 기본 설정
st.set_page_config(page_title="우주선 탈출 클릭커 PRO", page_icon="🚀", layout="centered")

# 1초(1000ms)마다 백그라운드 자동 갱신
st_autorefresh(interval=1000, key="clicker_game_refresh")

# --- 1. 게임 데이터 및 세션 초기화 ---
TARGET_GOLD = 1000000
PLAY_TIME_LIMIT = 900

if "gold" not in st.session_state:
    st.session_state.gold = 0
if "gold_per_click" not in st.session_state:
    st.session_state.gold_per_click = 1
if "auto_gold" not in st.session_state:
    st.session_state.auto_gold = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# 피버 타임 시스템 변수
if "fever_gauge" not in st.session_state:
    st.session_state.fever_gauge = 0      # 피버 게이지 (0~100)
if "fever_active" not in st.session_state:
    st.session_state.fever_active = False # 피버 타임 활성화 여부
if "fever_end_time" not in st.session_state:
    st.session_state.fever_end_time = 0   # 피버 타임 종료 예정 시각

# 황금 상자 시스템 변수
if "box_spawned" not in st.session_state:
    st.session_state.box_spawned = False  # 상점 등장 여부
if "box_expire_time" not in st.session_state:
    st.session_state.box_expire_time = 0  # 상자 소멸 예정 시각
if "box_gold_reward" not in st.session_state:
    st.session_state.box_gold_reward = 0  # 상자 보상 액수

# 상점 밸런스 비용
if "cost_click" not in st.session_state:
    st.session_state.cost_click = 15
if "cost_miner" not in st.session_state:
    st.session_state.cost_miner = 100
if "cost_factory" not in st.session_state:
    st.session_state.cost_factory = 1200

current_time = time.time()

# --- 2. 시간 흐름에 따른 게임 로직 처리 (1초마다 실행됨) ---

# A. 피버 타임 타이머 체크
if st.session_state.fever_active:
    if current_time >= st.session_state.fever_end_time:
        st.session_state.fever_active = False
        st.session_state.fever_gauge = 0

# B. 현재 배율 계산 (피버 타임 시 3배 버프 적용)
multiplier = 3 if st.session_state.fever_active else 1
current_turn_auto_gold = st.session_state.auto_gold * multiplier

# C. 자동 골드 획득 연산
st.session_state.gold += current_turn_auto_gold

# D. 황금 상자 생성 및 소멸 로직
if st.session_state.box_spawned:
    # 제한 시간이 지나면 상자 소멸
    if current_time >= st.session_state.box_expire_time:
        st.session_state.box_spawned = False
else:
    # 상자가 없는 상태라면 5% 확률로 돌발 스폰 (자동 생산량이 1 이상일 때부터 등장)
    if st.session_state.auto_gold > 0 and random.random() < 0.05:
        st.session_state.box_spawned = True
        st.session_state.box_expire_time = current_time + 7  # 7초 동안만 유지됨
        # 보상 규모: 현재 초당 생산량의 20배~40배 사이 무작위
        st.session_state.box_gold_reward = st.session_state.auto_gold * random.randint(20, 40)


# --- 3. 승리 / 패배 조건 연산 ---
elapsed_time = int(current_time - st.session_state.start_time)
remaining_time = PLAY_TIME_LIMIT - elapsed_time

def format_time(seconds):
    mins = max(0, seconds) // 60
    secs = max(0, seconds) % 60
    return f"{mins:02d}:{secs:02d}"

if st.session_state.gold >= TARGET_GOLD:
    st.balloons()
    st.title("🎉 탈출 성공!")
    st.success(f"축하합니다! **{format_time(elapsed_time)}**만에 탈출에 성공했습니다!")
    if st.button("게임 다시 시작하기"):
        st.session_state.clear()
        st.rerun()
    st.stop()

if remaining_time <= 0:
    st.title("💀 게임 오버 (탈출 실패)")
    st.error("15분의 제한시간이 지나 우주선이 폭발했습니다...")
    if st.button("다시 도전하기"):
        st.session_state.clear()
        st.rerun()
    st.stop()


# --- 4. 메인 UI 화면 그리기 ---
if st.session_state.fever_active:
    st.title("🔥 무한 피버 타임 진행 중!! (효율 3배) 🔥")
else:
    st.title("🚀 우주선 탈출 클릭커 (피버 & 황금상자)")

st.write(f"목표: 행성이 파괴되기 전에 **{TARGET_GOLD:,} G**를 모아 우주선 엔진을 가동하세요!")
st.divider()

# 대시보드 (시간 / 진행도 / 피버 게이지)
col_time, col_progress = st.columns()
with col_time:
    st.metric(label="⏳ 남은 시간", value=format_time(remaining_time))
with col_progress:
    progress_percentage = min(st.session_state.gold / TARGET_GOLD, 1.0)
    st.write(f"🛰️ 우주선 충전율: **{progress_percentage*100:.1f}%**")
    st.progress(progress_percentage)

# 피버 게이지 시각화
st.write(f"🔥 피버 에너지 게이지: **{st.session_state.fever_gauge}%**")
st.progress(st.session_state.fever_gauge / 100)

# 현재 스펙 디스플레이
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="💰 현재 골드", value=f"{st.session_state.gold:,} G")
with c2:
    st.metric(label="⚡ 클릭당 파워", value=f"+{st.session_state.gold_per_click * multiplier:,} G")
with c3:
    st.metric(label="🤖 초당 자동 생산", value=f"+{current_turn_auto_gold:,} G/s")

st.write("")

# 📦 [이벤트 추가] 황금 상자 실시간 UI 컴포넌트
if st.session_state.box_spawned:
    box_sec_left = int(st.session_state.box_expire_time - time.time())
    st.warning(f"📦 우주 미확인 황금 상자가 출현했습니다! (소멸까지 {box_sec_left}초)")
    # 상자 클릭 버튼
    if st.button(f"✨ 황금 상자 열기! (+{st.session_state.box_gold_reward:,} G 획득)", use_container_width=True):
        st.session_state.gold += st.session_state.box_gold_reward
        st.session_state.box_spawned = False
        st.success("대박! 보너스 자원을 획득했습니다!")
        st.rerun()

st.write("")

# 🔥 메인 수동 클릭 버튼
btn_label = "⚡ 피버 클릭!! (CLICK)" if st.session_state.fever_active else "⛏️ 에너지 광석 채굴! (CLICK)"
if st.button(btn_label, use_container_width=True, type="primary"):
    # 골드 획득 (피버 시 배율 반영)
    st.session_state.gold += (st.session_state.gold_per_click * multiplier)
    
    # 피버 게이지 상승 로직 (피버 타임이 아닐 때만 게이지 누적)
    if not st.session_state.fever_active:
        st.session_state.fever_gauge += 4  # 25번 클릭하면 100% 도달
        if st.session_state.fever_gauge >= 100:
            st.session_state.fever_active = True
            st.session_state.fever_end_time = time.time() + 10  # 10초간 지속
            st.toast("🔥 피버 타임 발동!!! 모든 생산력 3배!", icon="🔥")
            
    st.rerun()

st.divider()

# 🛒 상점 시스템 (사이드바)
st.sidebar.header("🛒 우주선 정비소 (상점)")

# 업그레이드 1: 클릭 강화
st.sidebar.subheader("💪 채굴 렌치 업그레이드")
st.sidebar.write(f"기본 클릭 효율 +2 | 가격: {st.session_state.cost_click:,} G")
if st.sidebar.button("구매하기", key="btn_click"):
    if st.session_state.gold >= st.session_state.cost_click:
        st.session_state.gold -= st.session_state.cost_click
        st.session_state.gold_per_click += 2
        st.session_state.cost_click = int(st.session_state.cost_click * 1.4)
        st.rerun()
    else:
        st.sidebar.error("골드가 부족합니다!")

# 업그레이드 2: 자동 드론
st.sidebar.subheader("🤖 자동 채굴 드론 배치")
st.sidebar.write(f"기본 초당 생산 +5 | 가격: {st.session_state.cost_miner:,} G")
if st.sidebar.button("고용하기", key="btn_miner"):
    if st.session_state.gold >= st.session_state.cost_miner:
        st.session_state.gold -= st.session_state.cost_miner
        st.session_state.auto_gold += 5
        st.session_state.cost_miner = int(st.session_state.cost_miner * 1.5)
        st.rerun()
    else:
        st.sidebar.error("골드가 부족합니다!")

# 업그레이드 3: 자동 발전소
st.sidebar.subheader("🏭 양자 에너지 발전소 건설")
st.sidebar.write(f"기본 초당 생산 +60 | 가격: {st.session_state.cost_factory:,} G")
if st.sidebar.button("건설하기", key="btn_factory"):
    if st.session_state.gold >= st.session_state.cost_factory:
        st.session_state.gold -= st.session_state.cost_factory
        st.session_state.auto_gold += 60
        st.session_state.cost_factory = int(st.session_state.cost_factory * 1.6)
        st.rerun()
    else:
        st.sidebar.error("골드가 부족합니다!")

# 게임 리셋
st.sidebar.write("")
if st.sidebar.button("⚠️ 처음부터 다시하기", type="secondary"):
    st.session_state.clear()
    st.rerun()
