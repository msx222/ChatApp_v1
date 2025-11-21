import streamlit as st

# =========================================================
# Streamlit Settings
# =========================================================
st.set_page_config(
    page_title="保安基準AI",
    page_icon="🚗",
    layout="wide"
)

# =========================================================
# ChatGPT風（中央幅）
# =========================================================
st.markdown("""
<style>
.block-container {
    max-width: 1000px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>
""", unsafe_allow_html=True)


# st.markdown("""
# <style>
#     /* Streamlit 標準ヘッダーを完全非表示 */
#     header[data-testid="stHeader"] {
#         display:true !important;
#     }
# </style>
# """, unsafe_allow_html=True)
#
# st.markdown("""
# <style>
#
#     /* サイドバー折りたたみ（collapse）ボタンを完全非表示 */
#     button[aria-label="Toggle sidebar"],
#     button[data-testid="stSidebarCollapseButton"],
#     span[data-testid="stSidebarToggleIcon"] {
#         display: none !important;
#         visibility: hidden !important;
#         pointer-events: none !important;
#     }
#
# </style>
# """, unsafe_allow_html=True)

NAVBAR_HEIGHT = 40

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
            z-index: 9999999;
        ">
            <img src="https://www.mitsubishielectric-mobility.com/assets_gws_template_responsive/img/logo_ja.svg"
                 style="height: 35px; margin-right: 12px;">
            <span style="font-size: 19px; font-weight: 600;">
                🚗 品情二 業務サポートAI (PoC版)
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

navbar()

# def navbar():
#     # 1) Navbar の HTML
#     st.markdown(
#         f"""
#         <div class="custom-navbar">
#             <img src="https://www.mitsubishielectric-mobility.com/assets_gws_template_responsive/img/logo_ja.svg"
#                  style="height: 35px; margin-right: 12px;">
#             <span class="navbar-title">
#                 🚗 品情二 業務サポートAI (PoC版)
#             </span>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     # 2) ライト/ダークテーマ切替 CSS
#     st.markdown(
#         f"""
#         <style>
#
#         /* ==== Navbar の共通スタイル ==== */
#         .custom-navbar {{
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: {NAVBAR_HEIGHT}px;
#             display: flex;
#             align-items: center;
#             padding: 0 25px;
#             z-index: 9999999;
#             border-bottom: 1px solid var(--border-color);
#             background-color: var(--bg-color);
#
#             color: var(--text-color);
#         }}
#
#         .navbar-title {{
#             font-size: 19px;
#             font-weight: 600;
#             color: var(--text-color);
#         }}
#
#         /* ==== Lightテーマ用 ==== */
#         body[data-theme="light"] {{
#             --bg-color: #ffffff;
#             --text-color: #000000;
#             --border-color: #dddddd;
#         }}
#
#         /* ==== Darkテーマ用 ==== */
#         body[data-theme="dark"] {{
#             --bg-color: #0e1117;
#             --text-color: #ffffff;
#             --border-color: #333333;
#         }}
#
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
#
# navbar()

# ==============================
# ★ ここがさっきエラー出てたところ（完全版CSS）
# ==============================
st.markdown(
    f"""
    <style>
        /* メイン側を下げる */
        div[data-testid="stAppViewContainer"] {{
            padding-top: {NAVBAR_HEIGHT + 1}px !important;
        }}

        section[data-testid="stMain"] {{
            padding-top: {NAVBAR_HEIGHT + 1}px !important;
        }}

        .block-container {{
            padding-top: {NAVBAR_HEIGHT + 1}px !important;
        }}


    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("""
<style>

    /* block-container の最大幅と揃える */
    div[data-testid="stChatInput"] {
        max-width: 740px !important;   /* Streamlitデフォルトのblock width */
        margin-left: auto !important;
        margin-right: auto !important;
    }

    textarea[data-testid="stChatInputTextArea"] {
        width: 100% !important;
    }

</style>
""", unsafe_allow_html=True)

# ==============================
# チャット部分（ダミー）
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    # st.title("💬 ChatGPT風UI Demo")
    mode = st.radio(
        "モード選択",
        ["通常チャット", "PDF解析（ダミー）", "技術基準判定（ダミー）"],
    )
    st.markdown("---")
    st.markdown("これは ChatGPT 風の UI を再現するためのデモです。")
    # Using object notation
    add_selectbox = st.sidebar.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone")
    )

    # Using "with" notation
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    color = st.select_slider(
        "Select a color of the rainbow",
        options=[
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "indigo",
            "violet",
        ],
    )

# st.title("ChatGPT風アプリ（デモ）")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("メッセージを入力してください", accept_file="multiple",):
    st.session_state.messages.append({"role": "user", "content": prompt})
    dummy_response = f"これは **{mode} モード** のダミー回答です。\n\n入力: `{prompt}`"
    st.session_state.messages.append({"role": "assistant", "content": dummy_response})
    st.rerun()
