import random
import streamlit as st

st.set_page_config(page_title="🎨 로또 번호 생성기", page_icon="🎰", layout="centered")

# 로또 공 모양 스타일링을 위한 CSS 정의
st.markdown("""
<style>
    .lotto-ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        color: white;
        font-weight: bold;
        font-size: 18px;
        margin: 3px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .ball-1 { background-color: #fbc02d; color: #333; } /* 1~10: 노란색 */
    .ball-2 { background-color: #1e88e5; }             /* 11~20: 파란색 */
    .ball-3 { background-color: #e53935; }             /* 21~30: 빨간색 */
    .ball-4 { background-color: #7cb342; }             /* 31~40: 초록색 */
    .ball-5 { background-color: #8e24aa; }             /* 41~45: 보라색 */
    
    .lotto-set {
        background-color: #f8f9fa;
        padding: 12px 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #4caf50;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

# 생성된 로또 번호 조합을 저장할 세션 상태 리스트 초기화
if "lotto_history" not in st.session_state:
    st.session_state.lotto_history = []

def get_ball_class(number):
    """숫자 범위에 따라 로또 공의 색상 클래스를 반환하는 함수"""
    if number <= 10:
        return "ball-1"
    elif number <= 20:
        return "ball-2"
    elif number <= 30:
        return "ball-3"
    elif number <= 40:
        return "ball-4"
    else:
        return "ball-5"

def render_lotto_balls(numbers):
    """숫자 리스트를 받아 HTML 공 태그 형태로 변환하는 함수"""
    balls_html = ""
    for num in numbers:
        color_class = get_ball_class(num)
        balls_html += f'<span class="lotto-ball {color_class}">{num}</span>'
    return balls_html

st.title("🎰 행운의 로또 번호 생성기")
st.write("버튼을 누르면 1~45 사이의 중복 없는 6개 숫자가 생성됩니다. (최대 5개까지 유지)")

col1, col2 = st.columns([2, 1])

with col1:
    # 로또 번호 생성 버튼 클릭 시 동작
    if st.button("🎲 로또번호 생성", use_container_width=True):
        # 1부터 45까지 중복 없이 6개 숫자 추출 후 오름차순 정렬
        new_numbers = sorted(random.sample(range(1, 46), 6))
        
        # 세션 상태 리스트의 맨 앞에 새 번호 추가 (최신 생성 번호가 위로)
        st.session_state.lotto_history.insert(0, new_numbers)
        
        # 5개가 넘어가면 가장 오래된 숫자를 지움 (FIFO)
        if len(st.session_state.lotto_history) > 5:
            st.session_state.lotto_history.pop()

with col2:
    # 전체 기록 삭제 버튼
    if st.button("🗑️ 기록 초기화", use_container_width=True):
        st.session_state.lotto_history = []
        st.rerun()

st.divider()

# 번호 조합 목록 출력
if st.session_state.lotto_history:
    st.subheader("📋 최근 생성된 번호 (최대 5개)")
    
    for idx, numbers in enumerate(st.session_state.lotto_history):
        balls_display = render_lotto_balls(numbers)
        # 최신 생성 조합에는 (최신) 표시 추가
        label = f"<b>Set {len(st.session_state.lotto_history) - idx}</b>"
        if idx == 0:
            label += ' <span style="color: #e53935; font-size: 12px;">(New)</span>'
            
        st.markdown(
            f'<div class="lotto-set"><div>{label}</div><div>{balls_display}</div></div>',
            unsafe_allow_html=True
        )
else:
    st.info("버튼을 눌러 로또 번호를 생성해 보세요!")