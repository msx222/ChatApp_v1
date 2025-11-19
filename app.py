import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# ================================
# Import Stub Workflows
# ================================
from src.workflows.technical.graph import technical_graph
from src.workflows.failure.graph import failure_graph
from src.workflows.law.graph import law_graph
from src.workflows.pdf.graph import pdf_graph
from src.workflows.general.graph import general_graph

# Router
from src.router.router_chain import classify_query

# UI Components
from ui.components.chat_display import render_chat, tool_selector, radio_with_tooltips
from ui.components.chat_input import render_input_box


# ================================
# Streamlit Settings
# ================================
st.set_page_config(
    page_title="保安基準AI",
    page_icon="🚗",
    layout="wide"
)
# =========================================================
# ChatGPT風「中央固定幅」CSS
# =========================================================
st.markdown(
    """
    <style>
    /* ページ全体の中央固定幅レイアウト */
    .block-container {
        max-width: 820px !important;   /* ChatGPTに近い幅 */
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# =========================================================
# ★ ③ 固定 NavBar（必ず CSS の後）
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
        background-color: #ffffff;
        border-bottom: 1px solid #dcdcdc;
        display: flex;
        align-items: center;
        padding: 0 25px;
        z-index: 99999999;
    ">
        <img src="https://www.mitsubishielectric-mobility.com/assets_gws_template_responsive/img/logo_ja.svg"
             style="height: 45px; margin-right: 12px;">
        <span style="font-size: 26px; font-weight:600;">🚗 品情二　業務サポートAI（PoC版）</span>
    </div>
    """, unsafe_allow_html=True)

navbar()


# ================================
# Session Initialization
# ================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "workflow_mode" not in st.session_state:
    st.session_state.workflow_mode = "自動判別"

if "show_mode_menu" not in st.session_state:
    st.session_state.show_mode_menu = False



# ================================
# ChatGPT風 入力UI（＋ボタン付き）
# ================================
def chat_input_with_mode_selector():

    col_plus, col_input = st.columns([0.08, 0.92])

    # + ボタン
    with col_plus:
        clicked = st.button("＋", key="open_menu", help="AIモードを選択")

    # テキスト入力
    with col_input:
        user_text = st.chat_input("メッセージを入力してください")

    return user_text, clicked



# ================================
# Workflow 実行
# ================================
def run_workflow(workflow_name: str, query: str):

    graphs = {
        "technical": technical_graph,
        "failure": failure_graph,
        "law": law_graph,
        "pdf": pdf_graph,
        "general": general_graph,
    }

    graph = graphs.get(workflow_name)
    if graph is None:
        return "エラー：対応するワークフローがありません。"

    result = graph.invoke({"user_query": query})
    return result.get("answer", "エラー：回答生成に失敗しました。")



# ================================
# UI：メイン画面
# ================================
# st.title("🚗 保安基準AI（統合ワークフロー版）")

# チャット表示
render_chat(st.session_state.messages)



# ================================
# 入力欄
# ================================
user_input, menu_clicked = chat_input_with_mode_selector()



# ================================
# モード選択メニュー
# ================================
if menu_clicked:
    # メニュー表示/非表示を切り替え
    st.session_state.show_mode_menu = not st.session_state.show_mode_menu

if st.session_state.show_mode_menu:

    # st.markdown("### 🔧 モード選択（エージェント選択）")
    # if st.session_state.show_mode_menu:
    #     tool_options = [
    #         "技術基準・適合判定",
    #         "PDF解析",
    #         "不具合解析",
    #         "法制度説明",
    #         "通常QA",
    #     ]
    #
    #     tool_desc = {
    #         "技術基準・適合判定": "部品名＋寸法から適合可否を判定します。",
    #         "PDF解析": "PDF・画像からテキスト抽出し基準判定に活用します。",
    #         "不具合解析": "症状から原因推定を行います。",
    #         "法制度説明": "道路運送車両法や制度を分かりやすく説明します。",
    #         "通常QA": "一般的な質問に対応するモードです。",
    #     }
    #
    #     selected = radio_with_tooltips(
    #         "使用するAIモード",
    #         tool_options,
    #         tool_desc,
    #         key="workflow_radio"
    #     )
    #     if selected:
    #         st.session_state.workflow_mode = selected

    st.session_state.workflow_mode = st.radio(
        "使用するAIモードを選択してください",
        options=[
            "自動判別",
            "技術基準・適合判定",
            "不具合解析",
            "法制度説明",
            "PDF解析",
            "通常QA",
        ],
        key="workflow_mode_radio",
    )



# ================================
# Query Handling
# ================================
if user_input:

    # 1. ユーザー発言の追加
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. ワークフロー決定
    mode = st.session_state.workflow_mode

    if mode == "自動判別":
        detected = classify_query(user_input)
        workflow = detected["workflow"]
    else:
        workflow = {
            "技術基準・適合判定": "technical",
            "不具合解析": "failure",
            "法制度説明": "law",
            "PDF解析": "pdf",
            "通常QA": "general"
        }.get(mode, "general")

    # 3. ワークフロー実行
    answer = run_workflow(workflow, user_input)

    # 4. AIメッセージとして追加
    st.session_state.messages.append({"role": "assistant", "content": answer})

    st.rerun()
