import streamlit as st

# def render_chat(messages):
#     for msg in messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])
import streamlit as st

def render_chat(messages):

    st.markdown(
        """
        <style>

        /* === 共通バブル === */
        .chat-bubble {
            background: #ffffff;
            padding: 16px 20px;
            border-radius: 12px;
            margin: 12px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,0,0,0.06);
            line-height: 1.6;
            font-size: 15px;
        }

        /* === ユーザー（右寄せ・小さめ） === */
        .bubble-right {
            display: flex;
            justify-content: flex-end;
            width: 100%;
        }

        .user-bubble {
            background: #f4f9ff;
            border: 1px solid #d5e8ff;
            max-width: 80%;      /* ユーザーは吹き出し風 */
        }

        /* === AI（幅いっぱいカード） === */
        .assistant-container {
            width: 100%;
            display: flex;
            justify-content: flex-start;
        }

        .assistant-bubble {
            width: 100%;         /* 左寄せではなく「幅いっぱい」 */
            background: #ffffff;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    for msg in messages:
        content = msg["content"].replace("\n", "<br>")

        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="bubble-right">
                    <div class="chat-bubble user-bubble">{content}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"""
                <div class="assistant-container">
                    <div class="chat-bubble assistant-bubble">{content}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ================================
# ChatGPT風 tool selector（説明付きカード UI）
# ================================
def tool_selector():

    st.markdown(
        """
        <style>
        /* （CSSは省略） */
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔧 モード選択（説明付きカード UI）")

    tool_map = {
        "🔧 基準判定・設計系": [
            ("技術基準・適合判定", "部品名＋寸法から適合可否を判定します。"),
            ("PDF解析", "PDF・画像からテキスト抽出し基準判定に活用します。"),
        ],
        "🧰 故障診断": [
            ("不具合解析", "症状から原因を推定し、対策を提案します。"),
        ],
        "📘 法制度・一般": [
            ("法制度説明", "法令や制度をわかりやすく説明します。"),
            ("通常QA", "一般的な質問に対応します。"),
        ],
    }

    selected = None

    for category, tools in tool_map.items():
        st.markdown(f"<div class='tool-category'>{category}</div>", unsafe_allow_html=True)
        for title, desc in tools:
            if st.button(f"{title}", key=f"tool_{title}"):
                selected = title
            st.markdown(
                f"""
                <div class="tool-card" onclick="document.getElementById('tool_{title}').click()">
                    <div class="tool-title">{title}</div>
                    <div class="tool-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    return selected

def radio_with_tooltips(label, options, descriptions, key):

    # CSS：ポップアップのスタイル
    st.markdown("""
    <style>
    .tooltip-container {
        position: relative;
        display: inline-block;
        width: 100%;
    }
    .tooltip-text {
        visibility: hidden;
        background-color: #333;
        color: #fff;
        text-align: left;
        padding: 6px 10px;
        border-radius: 6px;
        position: absolute;
        z-index: 100;
        left: 0;
        top: 105%;
        width: 260px;
        font-size: 12px;
        line-height: 1.4;
        opacity: 0;
        transition: opacity 0.15s ease;
    }
    .tooltip-container:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

    # カスタムラベルを構築
    display_labels = []
    for opt in options:
        desc = descriptions.get(opt, "")
        display_labels.append(
            f"""
            <div class="tooltip-container">
                {opt}
                <span class="tooltip-text">{desc}</span>
            </div>
            """
        )

    # Streamlit ラジオの表示
    # 「format_func」で HTML をそのまま描画
    selected = st.radio(
        label,
        options,
        key=key,
        format_func=lambda x: display_labels[options.index(x)],
    )

    return selected
