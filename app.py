import streamlit as st

# =========================================================
# Streamlit Settings
# =========================================================
st.set_page_config(
    page_title="保安基準AI",
    page_icon="🚗",
    layout="wide",
)

# =========================================================
# 中央幅（ChatGPT風）
# =========================================================
st.markdown("""
<style>
.block-container {
    max-width: 1100px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# Streamlit 標準ヘッダー非表示（安定）
# =========================================================
st.markdown("""
<style>
header[data-testid="stHeader"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)


NAVBAR_HEIGHT = 50

# ==============================
# 固定 Navbar
# ==============================
def navbar():
    st.markdown(
        f"""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: {NAVBAR_HEIGHT}px;
            background-color: white;
            border-bottom: 1px solid #ddd;
            display: flex;
            align-items: center;
            padding: 0 25px;
            z-index: 99999999;
        ">
            <img src="https://www.mitsubishielectric-mobility.com/assets_gws_template_responsive/img/logo_ja.svg"
                 style="height: 42px; margin-right: 12px;">
            <span style="font-size: 24px; font-weight: 600;">
                🚗 品情二 業務サポートAI（PoC版）
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

navbar()

# =========================================================
# Navbar 押し下げ
# =========================================================
st.markdown(
    f"""
<style>
div[data-testid="stAppViewContainer"] {{
    padding-top: {NAVBAR_HEIGHT + 5}px !important;
}}
section[data-testid="stMain"] {{
    padding-top: {NAVBAR_HEIGHT + 5}px !important;
}}
.block-container {{
    padding-top: {NAVBAR_HEIGHT + 5}px !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 入力欄をメインエリア幅に揃える
# =========================================================
st.markdown("""
<style>
/* ChatInput を中央幅に収める */
div[data-testid="stChatInput"] {
    max-width: 740px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# ＋ボタン UI（入力欄の左隣、下部固定）
# =========================================================

if "show_mode_popup" not in st.session_state:
    st.session_state.show_mode_popup = False

if "mode" not in st.session_state:
    st.session_state.mode = "通常チャット"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# ＋ボタンとポップアップの CSS
# ------------------------------
st.markdown("""
<style>

.chat-input-wrapper {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 740px;                     /* ChatInput と同じ幅 */
    display: flex;
    align-items: center;
    padding-bottom: 12px;
    z-index: 999999;
}

.plus-btn {
    width: 40px;
    height: 40px;
    margin-right: 8px;
    border-radius: 8px;
    border: 1px solid #ddd;
    background: #fff;
    font-size: 24px;
    line-height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.plus-btn:hover {
    background: #f2f2f2;
}

/* 上向きポップアップ */
.mode-popup {
    position: fixed;
    bottom: 65px;  /* ChatInput の真上に出る */
    left: 50%;
    transform: translateX(-50%);
    width: 280px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    z-index: 1000000;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------
# 入力欄と＋ボタン（下部固定）
# ------------------------------
st.markdown("<div class='chat-input-wrapper'>", unsafe_allow_html=True)

# ＋ボタン（左側）
if st.button("＋", key="plus_button"):
    st.session_state.show_mode_popup = not st.session_state.show_mode_popup

# chat_input（右側）
user_prompt = st.chat_input("メッセージを入力してください")

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# 上向きのポップアップ（ラジオ）
# ------------------------------
if st.session_state.show_mode_popup:
    st.markdown("<div class='mode-popup'>", unsafe_allow_html=True)
    st.write("📌 モード選択")
    st.session_state.mode = st.radio(
        "",
        ["通常チャット", "PDF解析（ダミー）", "技術基準判定（ダミー）"],
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# チャット処理
# =========================================================
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    reply = f"モード: **{st.session_state.mode}**\n\n入力: {user_prompt}"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.show_mode_popup = False
    st.rerun()

# =========================================================
# チャットログ
# =========================================================
st.title("ChatGPT風アプリ（デモ）")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

