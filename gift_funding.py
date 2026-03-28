import streamlit as st

st.set_page_config(page_title="생일 선물 펀딩", page_icon="🎉", layout="centered")

# -----------------------------
# 🎨 스타일
# -----------------------------
st.markdown("""
<style>
div[data-testid="stCodeBlock"] pre,
div[data-testid="stCodeBlock"] code {
    font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif !important;
    font-size: 16px !important;
}

div.stButton > button {
    border-radius: 12px;
    white-space: nowrap !important;
    min-height: 52px;
}

.participant-card {
    background-color: #fff7fb;
    border: 1px solid #f3d6e6;
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.participant-name {
    font-size: 18px;
    font-weight: 700;
    color: #d63384;
    margin-bottom: 4px;
}

.participant-amount {
    font-size: 16px;
    font-weight: 600;
    color: #333333;
    margin-bottom: 6px;
}

.participant-message {
    font-size: 15px;
    color: #555555;
    line-height: 1.5;
}

.final-amount-box {
    background-color: #fff8fc;
    border: 1.5px solid #f3d6e6;
    border-radius: 14px;
    padding: 14px 12px;
    margin: 10px 0 16px 0;
    text-align: center;
}

.final-amount-label {
    font-size: 14px;
    color: #888888;
    margin-bottom: 6px;
}

.final-amount-value {
    font-size: 24px;
    font-weight: 700;
    color: #d63384;
}

.section-caption {
    font-size: 15px;
    color: #666666;
    margin-top: -4px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🎁 생일자 정보 (여기만 수정)
# -----------------------------
BIRTHDAY_NAME = "린이"
TARGET_AMOUNT = 50000
GIFT_NAME = "산리오 무드등"
GIFT_LINK = "https://example.com"
BANK_NAME = "국민은행"
ACCOUNT_NUMBER = "41940204126414"
ACCOUNT_HOLDER = "마린"
KAKAOPAY_LINK = "https://example.com"
INTRO_MESSAGE = "린이의 스물두 번째 생일을 함께 축하해주세요 🎂"

# -----------------------------
# 🗂 세션 상태
# -----------------------------
if "participants" not in st.session_state:
    st.session_state.participants = []

if "selected_amount" not in st.session_state:
    st.session_state.selected_amount = 0

if "nickname_input" not in st.session_state:
    st.session_state.nickname_input = ""

if "message_input" not in st.session_state:
    st.session_state.message_input = ""

# -----------------------------
# 📊 펀딩 데이터 계산
# -----------------------------
total_paid = sum(p["amount"] for p in st.session_state.participants)
current_amount = total_paid
remaining = max(TARGET_AMOUNT - current_amount, 0)
progress = min(current_amount / TARGET_AMOUNT, 1.0) if TARGET_AMOUNT > 0 else 0

# -----------------------------
# 🎉 상단 영역
# -----------------------------
st.title(f"🎉 {BIRTHDAY_NAME} 생일 선물 펀딩")
st.write(INTRO_MESSAGE)
st.divider()

# -----------------------------
# 💖 원하는 선물
# -----------------------------
st.subheader("💖 원하는 선물")
st.write(f"**{GIFT_NAME}**")
st.link_button("🎁 선물 구경하기", GIFT_LINK)

st.divider()

# -----------------------------
# 📊 펀딩 현황
# -----------------------------
st.subheader("📊 펀딩 현황")

st.markdown(f"""
<h1 style='text-align: center;'>
💸 {current_amount:,}원
</h1>
<p style='text-align: center; font-size:18px;'>
목표 {TARGET_AMOUNT:,}원 중
</p>
""", unsafe_allow_html=True)

st.progress(progress)

if current_amount >= TARGET_AMOUNT:
    st.success("🎉 목표 달성! 최고다 진짜 🎁")
else:
    st.info(f"🎯 {remaining:,}원 남았어요!")

st.divider()

# -----------------------------
# 💳 입금 계좌 안내
# -----------------------------
st.subheader("💳 입금 안내")
st.write(f"**은행명:** {BANK_NAME}")
st.write(f"**계좌번호:** {ACCOUNT_NUMBER}")
st.write(f"**예금주:** {ACCOUNT_HOLDER}")

copy_text = f"{BANK_NAME} {ACCOUNT_NUMBER} ({ACCOUNT_HOLDER})"
st.code(copy_text, language=None)

st.link_button("💛 카카오페이로 바로 보내기", KAKAOPAY_LINK)
st.caption("📱 카카오페이 버튼은 휴대폰에서 이용해주세요")

st.divider()

# -----------------------------
# 💌 펀딩 참여하기
# -----------------------------
st.subheader("💌 펀딩 참여하기")

nickname = st.text_input("참여자 이름(닉네임)")

st.markdown("### 금액 선택하기")
st.markdown("<div class='section-caption'>자주 내는 금액을 눌러서 빠르게 선택할 수 있어요!</div>", unsafe_allow_html=True)

b1, b2, b3, b4, b5, spacer = st.columns([1.15, 1.15, 1.15, 1.15, 1.15, 6], gap="small")

with b1:
    if st.button("1천"):
        st.session_state.selected_amount = 1000
        st.rerun()
with b2:
    if st.button("5천"):
        st.session_state.selected_amount = 5000
        st.rerun()
with b3:
    if st.button("1만"):
        st.session_state.selected_amount = 10000
        st.rerun()
with b4:
    if st.button("2만"):
        st.session_state.selected_amount = 20000
        st.rerun()
with b5:
    if st.button("3만"):
        st.session_state.selected_amount = 30000
        st.rerun()

pay_amount = st.number_input(
    "직접 금액 입력하기",
    min_value=0,
    step=1000,
    value=st.session_state.selected_amount
)

st.session_state.selected_amount = int(pay_amount)

final_amount_text = "아직 입력되지 않았어요" if st.session_state.selected_amount == 0 else f"{st.session_state.selected_amount:,}원"

st.markdown(
    f"""
    <div class="final-amount-box">
        <div class="final-amount-label">최종 펀딩 금액</div>
        <div class="final-amount-value">{final_amount_text}</div>
    </div>
    """,
    unsafe_allow_html=True
)

message = st.text_input("축하의 메시지를 전해보세요!")

st.info("💡 카카오페이로 송금 후, 아래 버튼을 눌러주세요")

if st.button("💸 입금 완료했어요"):
    if nickname.strip() == "":
        st.warning("참여자 이름(닉네임)을 입력해주세요.")
    elif pay_amount <= 0:
        st.warning("금액을 1원 이상 입력해주세요.")
    else:
        st.session_state.participants.append({
            "name": nickname.strip(),
            "amount": int(pay_amount),
            "message": message.strip()
        })

        st.session_state.selected_amount = 0

        st.balloons()

        st.markdown(f"""
        <h3 style='text-align:center; color:#d63384;'>
        🍀 {nickname.strip()}님이 {int(pay_amount):,}원을 보태줬어요 🍀
        </h3>
        <p style='text-align:center; font-size:16px;'>
        덕분에 생일이 더 특별해졌어요 😊
        </p>
        """, unsafe_allow_html=True)

st.divider()
# -----------------------------
# 👥 참여자 목록
# -----------------------------
st.subheader("👥 고마운 사람들")
st.caption(f"총 {len(st.session_state.participants)}명 참여")

if len(st.session_state.participants) == 0:
    st.write("아직 참여자가 없어요.")
else:
    sorted_participants = sorted(
        st.session_state.participants,
        key=lambda x: x["amount"],
        reverse=True
    )

    for i, p in enumerate(sorted_participants, start=1):
        if p["message"]:
            card_html = f"""
            <div class="participant-card">
                <div class="participant-name">{i}. {p['name']}</div>
                <div class="participant-amount">💸 {p['amount']:,}원 보태줌</div>
                <div class="participant-message">💬 {p['message']}</div>
            </div>
            """
        else:
            card_html = f"""
            <div class="participant-card">
                <div class="participant-name">{i}. {p['name']}</div>
                <div class="participant-amount">💸 {p['amount']:,}원 보태줌</div>
            </div>
            """

        st.markdown(card_html, unsafe_allow_html=True)
