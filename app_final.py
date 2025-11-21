import streamlit as st
from dotenv import load_dotenv
from langchain_core.runnables import AddableDict
from openai import OpenAI
import os

# Load .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# =======================================
# ★ 法令適合判定AIワークフロー
# =======================================
from src.workflows.judgement_ai.graph import build_judgement_graph
# Chat UI Components
from ui.components.chat_display import render_chat

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
    max-width: 900px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>
""", unsafe_allow_html=True)


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

st.markdown("""
<style>

/* ==============================
   ChatGPT 風ユーザーバブル
   ============================== */

/* Chatメッセージの全体コンテナ */
.stChatMessage {
    padding: 0 !important;
    margin-bottom: 10px !important;
}

/* --- ユーザー（右寄せ） --- */
.stChatMessage[data-testid="stChatMessage-user"] {
    display: flex;
    justify-content: flex-end;  /* 右寄せ */
}

/* バブル本体 */
.stChatMessage[data-testid="stChatMessage-user"] .stChatMessageContent {
    background: #e7f3ff;               /* ChatGPTユーザー色(青系) */
    color: #1a1a1a !important;
    padding: 10px 14px;
    border-radius: 12px;
    max-width: 75%;                    /* ChatGPTの幅感 */
    border: 1px solid #c7e0ff;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
}

/* テキスト要素の余白調整 */
.stChatMessage[data-testid="stChatMessage-user"] .stMarkdown {
    margin: 0 !important;
    padding: 0 !important;
}


/* ==============================
   AI バブル（左寄せ）
   ============================== */
.stChatMessage[data-testid="stChatMessage-assistant"] {
    display: flex;
    justify-content: flex-start;
}

.stChatMessage[data-testid="stChatMessage-assistant"] .stChatMessageContent {
    background: #ffffff;
    padding: 10px 14px;
    border-radius: 12px;
    max-width: 85%;
    border: 1px solid #eee;
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}

.stChatMessage[data-testid="stChatMessage-assistant"] .stMarkdown {
    margin: 0 !important;
    padding: 0 !important;
}

</style>
""", unsafe_allow_html=True)



# ==============================
# チャット履歴
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# サイドバー（モード選択）
# ==============================
with st.sidebar:

    mode = st.radio(
        "✨AIモード選択",
        ["通常チャット", "法令適合判定", "PDF解析"],
    )
    st.markdown("---")
    # mode = st.radio(
    #     "🛠️自動化ツール",
    #     ["異議申請処理",],
    # )


# # ==============================
# # チャット履歴表示
# # ==============================
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# =========================================================
# Chat表示
# =========================================================
render_chat(st.session_state.messages)



# ==============================
# 入力処理
# ==============================
#  =========================================================
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



if prompt := st.chat_input("メッセージを入力してください", accept_file="multiple"):

    # ユーザー発言を履歴へ
    # st.session_state.messages.append({"role": "user", "content": prompt})
    user_text = prompt.text if hasattr(prompt, "text") else str(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })
    # -------------------------
    # ★ 法令適合判定モード
    # -------------------------
    if mode == "法令適合判定":
        graph = build_judgement_graph()

        with st.spinner("適合性を判定中…"):
            state = graph.invoke({"input_text": prompt})

        final = state["final_result"]
        md = generate_judgement_markdown(final)

        st.session_state.messages.append(
            {"role": "assistant", "content": md}
        )
        # ★★★ これがないと画面に反映されない ★★★
        st.rerun()

        # graph = build_judgement_graph()
        #
        # with st.spinner("法令適合性を判定中…"):
        #     result_state = graph.invoke({"input_text": prompt})
        #
        # final = result_state["final_result"]
        #
        # # ★ 判定結果をそのまま会話に追加
        # output_text = "### 📘 法令適合判定 結果\n"
        #
        # for art in final["articles"]:
        #     output_text += f"#### {art['article']}（{art['title']}）\n"
        #     for cl in art["clauses"]:
        #         output_text += f"- **{cl['clause']}：{cl['overall']}**\n"
        #         for req in cl["requirements"]:
        #             output_text += f"    - R{req['req_id']} {req['text']}\n"
        #             output_text += f"        - 判定：{req['judgement']}\n"
        #             output_text += f"        - 信頼度：{req['confidence']:.2f}\n"
        #             output_text += f"        - 理由：{req['reasoning']}\n"
        #
        # st.session_state.messages.append({
        #     "role": "assistant",
        #     "content": output_text
        # })

    # -------------------------
    # 通常チャット / PDF解析 → GPT 応答
    # -------------------------
    else:
        # -------------------------
        # 通常チャット / PDF解析 → GPT 応答
        # -------------------------
        from openai import OpenAI

        client = OpenAI()

        # ChatInputValue → 純テキストへ変換
        user_text = prompt.text if hasattr(prompt, "text") else str(prompt)
        with st.spinner("LLMへ問い合わせ中…"):
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": f"あなたは '{mode}' モードのAIアシスタントです。",
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text}
                        ]
                    },
                ],
                temperature=0.2,
            )
            gpt_answer = completion.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": gpt_answer}
        )
        # ★★★ これがないと画面に反映されない ★★★
        st.rerun()
    # # -------------------------
    # # 通常チャット / PDF解析（ダミー）
    # # -------------------------
    # else:
    #     dummy_response = f"これは **{mode} モード** のダミー回答です。\n\n入力: `{prompt}`"
    #     st.session_state.messages.append({"role": "assistant", "content": dummy_response})

