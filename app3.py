import streamlit as st
from dotenv import load_dotenv
import os

# Load .env from root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# ================================
# Import Workflows
# ================================
from src.workflows.technical.graph import technical_graph
from src.workflows.failure.graph import failure_graph
from src.workflows.law.graph import law_graph
from src.workflows.pdf.graph import pdf_graph
from src.workflows.general.graph import general_graph

# 判定AIワークフロー（あなたの LangGraph + RAG Dummy）
from src.workflows.judgement_ai.graph import build_judgement_graph

# Router
from src.router.router_chain import classify_query

# Chat UI Components
from ui.components.chat_display import render_chat
from ui.components.chat_input import render_input_box


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
    max-width: 1100px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 固定 Navbar（復活版）
# =========================================================
NAVBAR_HEIGHT = 60

def navbar():
    st.markdown(f"""
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
             style="height: 42px; margin-right: 12px;">
        <span style="font-size: 24px; font-weight: 600;">
            🚗 品情二 業務サポートAI（PoC版）
        </span>
    </div>
    """, unsafe_allow_html=True)

navbar()

# Main コンテンツを Navbar 分下に下げる
st.markdown(f"""
<style>
.block-container {{
    padding-top: {NAVBAR_HEIGHT + 20}px !important;
}}
</style>
""", unsafe_allow_html=True)


# =========================================================
# Session State
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "workflow_mode" not in st.session_state:
    st.session_state.workflow_mode = "自動判別"

if "show_menu" not in st.session_state:
    st.session_state.show_menu = False


# =========================================================
# 判定結果 → Markdown に変換（過去事例つき）
# =========================================================
def generate_judgement_markdown(final_result):
    md = []
    overall = final_result["overall_judgement"]

    md.append(f"#### 📘 技術基準・適合判定（総合判定：{overall}）\n")

    for art in final_result["articles"]:
        md.append("---\n")
        pdf = art.get("pdf_url")
        md.append(f"##### {art['article']}（{art['title']}）")
        if pdf:
            md.append(f"🔗 [PDFリンクを見る]({pdf})\n")

        for cl in art["clauses"]:
            md.append(f"###### ● {cl['clause']}：{cl['overall']}")
            for req in cl["requirements"]:
                md.append(f"""
- **R{req["req_id"]}**: {req["text"]}
    - 判定: {req["judgement"]}
    - 信頼度: {req["confidence"]:.2f}
    - 理由: {req["reasoning"]}
""")

    # ---- 過去事例（今はダミー：将来RAG） ----
    md.append("---")
    md.append("#### 🛠 過去・類似不具合事例（参考）")

    past_cases = [
        {"year": 2022, "title": "前照灯 青色点灯の不適合", "category": "灯火",
         "desc": "青色LEDが原因で不適合。"},
        {"year": 2021, "title": "制動灯 光度不足", "category": "灯火",
         "desc": "光度が基準値不足で不適合。"}
    ]

    for case in past_cases:
        md.append(f"""
##### ● {case["year"]}年「{case["title"]}」
- 区分：{case["category"]}
- 内容：{case["desc"]}
""")

    return "\n".join(md)



# =========================================================
# Chat表示
# =========================================================
render_chat(st.session_state.messages)


# =========================================================
# 入力欄（＋モード選択）
# =========================================================
def chat_ui_row():
    col_plus, col_input = st.columns([0.08, 0.92])

    with col_plus:
        menu = st.button("＋", key="menu")

    with col_input:
        msg = st.chat_input("メッセージを入力してください",
            accept_file="multiple",
            # file_type=ALLOWED_FILE_TYPES
        )

    return msg, menu

user_msg, menu_clicked = chat_ui_row()


# モードメニュー
if menu_clicked:
    st.session_state.show_menu = not st.session_state.show_menu

if st.session_state.show_menu:
    st.session_state.workflow_mode = st.radio(
        "AIモードを選択してください",
        [
            "自動判別",
            "技術基準・適合判定",
            "不具合解析",
            "法制度説明",
            "PDF解析",
            "通常QA",
        ]
    )


# =========================================================
# 入力メッセージ処理
# =========================================================
if user_msg:

    # ユーザーバブルとしてチャットに追加
    st.session_state.messages.append({"role": "user", "content": user_msg})

    # 自動判別
    mode = st.session_state.workflow_mode
    if mode == "自動判別":
        detect = classify_query(user_msg)
        workflow = detect["workflow"]
    else:
        workflow = {
            "技術基準・適合判定": "judgement",
            "不具合解析": "failure",
            "法制度説明": "law",
            "PDF解析": "pdf",
            "通常QA": "general",
        }.get(mode, "general")

    # 判定AI（フル出力 → チャットに Markdown）
    if workflow == "judgement":
        graph = build_judgement_graph()

        with st.spinner("適合性を判定中…"):
            state = graph.invoke({"input_text": user_msg})

        final = state["final_result"]
        md = generate_judgement_markdown(final)

        st.session_state.messages.append(
            {"role": "assistant", "content": md}
        )

    else:
        # その他の通常QA系
        graphs = {
            "failure": failure_graph,
            "law": law_graph,
            "pdf": pdf_graph,
            "general": general_graph,
        }
        graph = graphs[workflow]

        with st.spinner("AIが回答生成中…"):
            result = graph.invoke({"user_query": user_msg})

        answer = result.get("answer", "応答生成に失敗しました。")
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    st.rerun()
