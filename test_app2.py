import streamlit as st
import json

st.set_page_config(page_title="保安基準AI", page_icon="🚗", layout="wide")

# ----------------------------------------------------
# セッション変数
# ----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "通常チャット"

if "show_mode" not in st.session_state:
    st.session_state.show_mode = False

if "js_event" not in st.session_state:
    st.session_state.js_event = None


# ----------------------------------------------------
# チャットログ
# ----------------------------------------------------
st.title("ChatGPT 完全再現 UI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ----------------------------------------------------
# HTML/CSS/JS 直接描画（iframe なし）
# ----------------------------------------------------
st.markdown("""
<style>

.chat-wrapper {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 740px;
    padding: 12px 20px;
    background: rgba(255,255,255,0.90);
    backdrop-filter: blur(8px);
    border-radius: 20px;
    border: 1px solid rgba(0,0,0,0.08);
    box-shadow: 0 -2px 25px rgba(0,0,0,0.15);
    z-index: 99999;
}

.chat-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.plus-btn {
    width: 44px;
    height: 44px;
    border-radius: 44px;
    border: 1px solid #ddd;
    background: white;
    font-size: 22px;
    cursor: pointer;
}

#msg {
    flex: 1;
    min-height: 30px;
    padding: 8px 16px;
    font-size: 16px;
    border-radius: 12px;
    border: 1px solid #ddd;
    resize: vertical;
}

.mode-popup {
    position: fixed;
    bottom: 90px;
    left: 50%;
    transform: translateX(-50%);
    width: 260px;
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #ddd;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    z-index: 1000000;
}

.mode-popup button {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    background: #fafafa;
}

</style>

<div class="chat-wrapper">
    <div class="chat-row">
        <!-- ★ toggle_mode → toggle に統一 -->
        <button class="plus-btn" onclick="sendEvent('toggle', '')">＋</button>
        <textarea id="msg" placeholder="メッセージを入力…"></textarea>
    </div>
</div>

<script>

// textarea 自動伸縮
const textarea = document.getElementById("msg");
textarea.addEventListener("input", function(){
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});

// Enter送信
textarea.addEventListener("keydown", function(e){
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendEvent("send", textarea.value);
        textarea.value = "";
        textarea.style.height = "40px";
    }
});

// ★ JS → Python は query params で統一
function sendEvent(action, text) {
    const payload = JSON.stringify({action: action, text: text});
    const url = new URL(window.location.href);
    url.searchParams.set("streamlit_js_event", payload);
    window.location.href = url.toString();
}

</script>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# JS → Python イベント受信
# ----------------------------------------------------
raw = st.query_params.get("streamlit_js_event")
if raw:
    st.session_state.js_event = json.loads(raw[0])
    st.query_params.clear()


# ----------------------------------------------------
# Python側イベント処理
# ----------------------------------------------------
if st.session_state.js_event:

    action = st.session_state.js_event["action"]
    text = st.session_state.js_event["text"]

    if action == "toggle":
        # ★ ポップアップ表示切替
        st.session_state.show_mode = not st.session_state.show_mode

    elif action == "send":
        st.session_state.messages.append({"role": "user", "content": text})
        st.session_state.messages.append(
            {"role": "assistant", "content": f"モード: **{st.session_state.mode}**\n\n{text}"}
        )

    elif action == "select_mode":
        st.session_state.mode = text
        st.session_state.show_mode = False

    st.session_state.js_event = None
    st.rerun()


# ----------------------------------------------------
# モード選択ポップアップ（＋で開く）
# ----------------------------------------------------
if st.session_state.show_mode:
    st.markdown("""
    <div class="mode-popup">
        <b>📌 モード選択</b><br><br>
        <button onclick="sendEvent('select_mode','通常チャット')">通常チャット</button>
        <button onclick="sendEvent('select_mode','PDF解析（ダミー）')">PDF解析（ダミー）</button>
        <button onclick="sendEvent('select_mode','技術基準判定（ダミー）')">技術基準判定（ダミー）</button>
    </div>
    """, unsafe_allow_html=True)
