import streamlit as st
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import random

st.set_page_config(page_title="생일 선물 펀딩", page_icon="🎉", layout="centered")

# -----------------------------
# 🗂 세션 상태
# -----------------------------
if "success_message" not in st.session_state:
    st.session_state.success_message = ""

if "nickname_input" not in st.session_state:
    st.session_state.nickname_input = ""

if "message_input" not in st.session_state:
    st.session_state.message_input = ""

if "custom_amount" not in st.session_state:
    st.session_state.custom_amount = 0

if "clear_form" not in st.session_state:
    st.session_state.clear_form = False

# -----------------------------
# 📡 구글 시트 연결
# -----------------------------
@st.cache_resource
def connect_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open("고마운사람들기록")
    worksheet = spreadsheet.worksheet("thanks")
    return worksheet

ws = connect_sheet()

# -----------------------------
# 🎨 스타일
# -----------------------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #fff0f6 0%, #fff8fc 45%, #ffffff 100%);
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 0 !important;
}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem;
    max-width: 760px;
}

header, #MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
}

div[data-testid="stCodeBlock"] pre,
div[data-testid="stCodeBlock"] code {
    font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif !important;
    font-size: 16px !important;
}

div.stButton > button {
    border-radius: 14px;
    white-space: nowrap !important;
    height: 44px !important;
    min-height: 44px !important;
    font-weight: 600;
    border: none;
    background: linear-gradient(135deg, #f8a5c2, #f78fb3);
    color: white;
    box-shadow: 0 4px 10px rgba(247, 143, 179, 0.25);
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #f78fb3, #f368a6);
    color: white;
}

.hero-wrap {
    text-align: center;
    margin: 30px 0 20px 0;
}

.hero-title {
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    color: #d63384;
    margin-bottom: 8px;
}

.hero-subtitle {
    text-align: center;
    font-size: 16px;
    color: #666;
    line-height: 1.6;
    margin-bottom: 6px;
}

.gift-card {
    background: linear-gradient(135deg, #fff7fb, #ffffff);
    border: 1px solid #f3d6e6;
    border-radius: 18px;
    padding: 18px 16px;
    text-align: center;
}

.amount-hero {
    background: linear-gradient(135deg, #fff7fb, #ffffff);
    border: 1.5px solid #f3d6e6;
    border-radius: 22px;
    padding: 22px 16px;
    text-align: center;
    margin: 8px 0 14px 0;
    box-shadow: 0 6px 18px rgba(214, 51, 132, 0.06);
}

.amount-hero-label {
    font-size: 14px;
    color: #888;
    margin-bottom: 8px;
}

.amount-hero-value {
    font-size: 42px;
    font-weight: 800;
    color: #d63384;
    line-height: 1.2;
}

.amount-hero-target {
    margin-top: 8px;
    font-size: 16px;
    color: #666;
}

.account-box {
    background: linear-gradient(135deg, #fff8fc, #ffffff);
    border: 1px solid #f3d6e6;
    border-radius: 18px;
    padding: 16px;
    margin-top: 10px;
}

.final-amount-box {
    background-color: #fff8fc;
    border: 1.5px solid #f3d6e6;
    border-radius: 16px;
    padding: 18px 12px;
    margin: 10px 0 14px 0;
    text-align: center;
}

.final-amount-label {
    font-size: 14px;
    color: #888888;
    margin-bottom: 6px;
}

.final-amount-value {
    font-size: 30px;
    font-weight: 700;
    color: #d63384;
}

.helper-text {
    font-size: 14px;
    color: #777777;
    margin-top: -2px;
    margin-bottom: 10px;
}

.small-muted {
    font-size: 13px;
    color: #888;
}

.custom-line {
    border: none;
    border-top: 1px solid #f3d6e6;
    margin: 20px 0;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    border-radius: 14px !important;
}

.success-box {
    background: #fff0f6;
    border: 1.5px solid #f8bbd0;
    color: #d63384;
    padding: 14px 16px;
    border-radius: 14px;
    font-weight: 700;
    margin: 8px 0 16px 0;
    text-align: center;
}

/* 반짝이 */
@keyframes twinkle {
    0% {
        transform: scale(1);
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.20);
    }
    100% {
        transform: scale(1.015);
        box-shadow: 0 0 24px rgba(255, 215, 0, 0.45);
    }
}

/* 공통 랭킹 카드 */
.rank-card {
    padding: 18px;
    border-radius: 20px;
    margin-bottom: 14px;
    border: 1px solid #f1d6e4;
    background: #ffffff;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.04);
}

.rank-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 800;
    padding: 6px 10px;
    border-radius: 999px;
    margin-bottom: 10px;
}

.rank-name {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 4px;
}

.rank-amount {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 8px;
}

.rank-message {
    font-size: 15px;
    line-height: 1.5;
}

.rank-time {
    font-size: 12px;
    color: #999;
    margin-top: 10px;
}

/* 1등 */
.rank-gold {
    background: linear-gradient(135deg, #fff8d6, #ffe082, #ffd54f);
    border: 2px solid #f4c542;
    animation: twinkle 1.6s infinite alternate;
}

.rank-gold .rank-badge {
    color: #7a5600;
    background: rgba(255, 255, 255, 0.58);
}

.rank-gold .rank-name,
.rank-gold .rank-amount,
.rank-gold .rank-message {
    color: #5f4300;
}

/* 2등 */
.rank-silver {
    background: linear-gradient(135deg, #f8f9fb, #e4e8ee, #cfd6df);
    border: 2px solid #b8c2cc;
}

.rank-silver .rank-badge {
    color: #4f5b66;
    background: rgba(255, 255, 255, 0.72);
}

.rank-silver .rank-name,
.rank-silver .rank-amount,
.rank-silver .rank-message {
    color: #3f4a54;
}

/* 3등 핑크 브론즈 */
.rank-bronze {
    background: linear-gradient(135deg, #fff1f5, #f7c3d3, #d89ab2);
    border: 2px solid #d58aa7;
}

.rank-bronze .rank-badge {
    color: #7b3f59;
    background: rgba(255, 255, 255, 0.72);
}

.rank-bronze .rank-name,
.rank-bronze .rank-amount,
.rank-bronze .rank-message {
    color: #6b314c;
}

/* 일반 카드 */
.rank-normal {
    background: #ffffff;
    border: 1px solid #f1d6e4;
}

.rank-normal .rank-badge {
    color: #d63384;
    background: #fff0f6;
}

.rank-normal .rank-name {
    color: #333333;
}

.rank-normal .rank-amount {
    color: #d63384;
}

.rank-normal .rank-message {
    color: #666666;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🎁 생일자 정보
# -----------------------------
BIRTHDAY_NAME = "린이"
TARGET_AMOUNT = 50000
GIFT_NAME = "산리오 무드등"
GIFT_LINK = "https://example.com"
BANK_NAME = "국민은행"
ACCOUNT_NUMBER = "41940204126414"
ACCOUNT_HOLDER = "마린"
INTRO_MESSAGE = "린이의 스물두 번째 생일을 함께 축하해주세요 🎂🎉"

THANK_YOU_MESSAGES = [
    "정말 고마워요 💖",
    "덕분에 생일이 더 특별해졌어요 🎂",
    "마음 보태줘서 너무 고마워요 🌷",
    "따뜻한 마음 전해줘서 고마워요 💕",
    "덕분에 좋은 하루가 될 것 같아요 😊",
    "함께해줘서 정말 감사해요 💖",
    "소중한 마음 너무 고마워요 🫶",
    "이렇게 챙겨줘서 정말 고마워요 🎁",
    "덕분에 더 행복한 생일이에요 💗",
    "마음 써줘서 진심으로 감사해요 🌸"
]

# -----------------------------
# 🔧 시트 값 안전하게 읽는 함수
# -----------------------------
def pick_value(row, keys, default=""):
    for key in keys:
        if key in row and row[key] not in [None, ""]:
            return row[key]
    return default

def pick_amount(row):
    raw = pick_value(row, ["금액", "입금 금액", "amount"], 0)
    try:
        return int(raw)
    except:
        try:
            return int(str(raw).replace(",", "").replace("원", "").strip())
        except:
            return 0

# -----------------------------
# 📊 구글 시트 데이터 불러오기
# -----------------------------
records = ws.get_all_records()
participants = []

for row in records:
    participants.append({
        "name": pick_value(row, ["닉네임", "이름", "참여자 이름", "name"], "익명"),
        "amount": pick_amount(row),
        "message": pick_value(row, ["메시지", "편지", "message"], ""),
        "time": pick_value(row, ["시간", "timestamp", "time"], "")
    })

current_amount = sum(p["amount"] for p in participants)
remaining = max(TARGET_AMOUNT - current_amount, 0)
progress = min(current_amount / TARGET_AMOUNT, 1.0) if TARGET_AMOUNT > 0 else 0

# -----------------------------
# 🎉 상단 영역
# -----------------------------
st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="hero-title">{BIRTHDAY_NAME} 생일 선물 펀딩</div>
        <div class="hero-subtitle">{INTRO_MESSAGE}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 💖 원하는 선물
# -----------------------------
st.subheader("💖 원하는 선물")
st.markdown(
    f"""
    <div class="gift-card">
        <div style="font-size:22px; font-weight:700; color:#d63384; margin-bottom:8px;">
            {GIFT_NAME}
        </div>
        <div class="small-muted">마음을 모아 선물해요🥳</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")
st.markdown(
    "<div style='font-size:14px; color:#777; text-align:center; margin-bottom:8px;'>원하는 선물이 궁금하면 아래 버튼을 눌러주세요.</div>",
    unsafe_allow_html=True
)
st.link_button("🎁 선물 구경하기", GIFT_LINK, use_container_width=True)

st.markdown('<hr class="custom-line">', unsafe_allow_html=True)

# -----------------------------
# 📊 펀딩 현황
# -----------------------------
st.subheader("📊 펀딩 현황")

st.markdown(
    f"""
    <div class="amount-hero">
        <div class="amount-hero-label">현재 모인 금액</div>
        <div class="amount-hero-value">💸 {current_amount:,}원</div>
        <div class="amount-hero-target">목표 {TARGET_AMOUNT:,}원 중</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.progress(progress)

percent = int(progress * 100)

if percent < 50:
    progress_msg = "아직 여유 있어요 😆"
elif percent < 80:
    progress_msg = "거의 다 왔어요 🔥"
elif percent < 100:
    progress_msg = "조금만 더!! 💪"
else:
    progress_msg = "목표 달성 🎉"

st.markdown(
    f"<div style='text-align:center; font-weight:600; color:#d63384; margin-top:6px;'>{percent}% 달성 · {progress_msg}</div>",
    unsafe_allow_html=True
)

if current_amount >= TARGET_AMOUNT:
    st.success("🎉 목표 달성! 최고다 진짜 🎁")
else:
    st.info(f"🎯 {remaining:,}원 남았어요!")

st.markdown('<hr class="custom-line">', unsafe_allow_html=True)

# -----------------------------
# 💳 입금 안내
# -----------------------------
st.subheader("💳 입금 안내")

st.markdown(
    f"""
    <div class="account-box">
        <div><b>은행명:</b> {BANK_NAME}</div>
        <div><b>계좌번호:</b> {ACCOUNT_NUMBER}</div>
        <div><b>예금주:</b> {ACCOUNT_HOLDER}</div>
    </div>
    """,
    unsafe_allow_html=True
)

copy_text = f"{BANK_NAME} {ACCOUNT_NUMBER} ({ACCOUNT_HOLDER})"
st.code(copy_text, language=None)
st.caption("클릭하면 계좌번호가 복사돼요 📋")

st.markdown("### 📌 입금 후 안내")
st.info("💡 입금 후 아래에서 금액과 메시지를 기록해주세요.\n입금자명은 닉네임과 맞추면 확인이 더 쉬워요.")

st.write("")
st.markdown("### 💛 카카오페이 송금")

KAKAOPAY_LINK = "https://qr.kakaopay.com/FHcm3jolo"
st.link_button("💛 카카오페이로 바로 송금하기", KAKAOPAY_LINK, use_container_width=True)
st.info("💡 카카오페이로 송금한 뒤, 아래에서 금액과 메시지를 기록해주세요.")

base_dir = Path(__file__).resolve().parent
qr_candidates = list(base_dir.glob("qr.*"))

if qr_candidates:
    st.image(str(qr_candidates[0]), width=320)
    st.caption("📱 QR 스캔해서 송금해주세요")
else:
    st.error("QR 이미지 파일을 찾을 수 없어요. 파일명을 qr.png 또는 qr.jpg로 맞춰주세요.")

st.markdown('<hr class="custom-line">', unsafe_allow_html=True)

# -----------------------------
# 💸 펀딩 참여 인증하기
# -----------------------------
st.subheader("💸 펀딩 참여 인증하기")

# 성공 메시지 표시
if st.session_state.get("success_message", ""):
    st.markdown(
        f"""
        <div class="success-box">
            🎉 {st.session_state.success_message}
        </div>
        """,
        unsafe_allow_html=True
    )

# 제출 후 폼 초기화
if st.session_state.get("clear_form", False):
    st.session_state["nickname_input"] = ""
    st.session_state["message_input"] = ""
    st.session_state["custom_amount"] = 0
    st.session_state["clear_form"] = False

nickname = st.text_input(
    "참여자 이름 (닉네임)",
    key="nickname_input"
)

st.markdown(
    "<div style='font-size:18px; font-weight:400; margin-top:10px; margin-bottom:6px; text-align:left;'>입금한 금액</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<div class='helper-text'>기록한 금액은 아래 ‘고마운 사람들’ 목록에 표시돼요.</div>",
    unsafe_allow_html=True
)

cols = st.columns(5, gap="small")
amounts = [1000, 5000, 10000, 20000, 30000]

for idx, amount in enumerate(amounts):
    with cols[idx]:
        if st.button(f"{amount:,}", key=f"amt_{amount}", use_container_width=True):
            st.session_state.custom_amount = amount
            st.rerun()

custom_amount = st.number_input(
    "직접 금액 입력하기",
    min_value=0,
    step=1000,
    key="custom_amount"
)

final_amount = int(custom_amount)

if final_amount > 0:
    final_amount_text = f"{final_amount:,}원"
    st.markdown(
        f"<div style='text-align:center; color:#d63384; font-weight:600;'>선택된 금액: {final_amount:,}원</div>",
        unsafe_allow_html=True
    )
else:
    final_amount_text = "아직 입력되지 않았어요"

st.markdown(
    f"""
    <div class="final-amount-box">
        <div class="final-amount-label">최종 펀딩 금액</div>
        <div class="final-amount-value">{final_amount_text}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div style='font-size:18px; font-weight:400; margin-top:10px;'>편지 남기기</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<div style='font-size:14px; color:#777; margin-bottom:-10px;'>축하 메시지를 남겨주세요 💖</div>",
    unsafe_allow_html=True
)

message = st.text_area(
    "",
    height=110,
    placeholder="생일 축하해! 즐거운 하루 보내 💕",
    key="message_input"
)

st.write("")

if st.button("💌 선물 보내고 기록하기", use_container_width=True):
    if nickname.strip() == "":
        st.warning("닉네임을 입력해주세요🥺")
    elif final_amount <= 0:
        st.warning("금액을 1원 이상 입력해주세요🥺")
    else:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ws.append_row([
            nickname.strip(),
            final_amount,
            message.strip(),
            now
        ])

        st.session_state.clear_form = True
        st.session_state.success_message = random.choice(THANK_YOU_MESSAGES)
        st.balloons()
        st.rerun()

st.markdown('<hr class="custom-line">', unsafe_allow_html=True)

# -----------------------------
# 👥 참여자 목록
# -----------------------------
st.subheader("👥 고마운 사람들")

# 방금 append_row 반영되도록 다시 읽기
records = ws.get_all_records()
participants = []

for row in records:
    participants.append({
        "name": pick_value(row, ["닉네임", "이름", "참여자 이름", "name"], "익명"),
        "amount": pick_amount(row),
        "message": pick_value(row, ["메시지", "편지", "message"], ""),
        "time": pick_value(row, ["시간", "timestamp", "time"], "")
    })

if participants:
    sorted_participants = sorted(participants, key=lambda x: x["amount"], reverse=True)

    for i, p in enumerate(sorted_participants, start=1):
        name = p["name"] if str(p["name"]).strip() else "익명"
        amount = p["amount"]
        msg = p["message"] if str(p["message"]).strip() else "축하 마음을 전했어요! 💕"
        time_text = p["time"]

        if i == 1:
            card_class = "rank-gold"
            badge = "🥇 1등"
            title = f"🥇 {name}"
        elif i == 2:
            card_class = "rank-silver"
            badge = "🥈 2등"
            title = f"🥈 {name}"
        elif i == 3:
            card_class = "rank-bronze"
            badge = "🥉 3등"
            title = f"🥉 {name}"
        else:
            card_class = "rank-normal"
            badge = f"{i}등"
            title = f"{name}"
        st.markdown(
            f"""
            <div class="rank-card {card_class}">
                <div class="rank-badge">{badge}</div>
                <div class="rank-name">{title}</div>
                <div class="rank-amount">{amount:,}원</div>
                <div class="rank-message">💌 {msg}</div>
                <div class="rank-time">{time_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("아직 기록된 사람이 없어요!")

st.markdown('<hr class="custom-line">', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color:#888; font-size:14px;'>함께 축하해줘서 정말 고마워 🥹💖</div>",
    unsafe_allow_html=True
)

