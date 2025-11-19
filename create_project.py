import os

# -----------------------------
# 必要なフォルダ構成
# -----------------------------
FOLDERS = [
    "src/router",
    "src/workflows/technical",
    "src/workflows/failure",
    "src/workflows/law",
    "src/workflows/pdf",
    "src/workflows/general",
    "ui/components",
]

# -----------------------------
# 作成するファイル（スタブ内容付き）
# -----------------------------
FILES = {
    "app.py": """\
# app.py は ChatGPTから生成した内容を貼り付けてください。
print("app.py が作成されました。内容は ChatGPT のコードを貼り付けて仕上げてください。")
""",

    # Router stub
    "src/router/router_chain.py": """\
def classify_query(text: str):
    \"\"\"スタブ版のルーター：簡易キーワード分類\"\"\"
    if "振動" in text or "異音" in text:
        return {"workflow": "failure"}
    if "条文" in text or "法" in text:
        return {"workflow": "law"}
    if "PDF" in text:
        return {"workflow": "pdf"}
    if "基準" in text or "寸法" in text:
        return {"workflow": "technical"}

    return {"workflow": "general"}
""",

    # ---- Workflows (Stub Graphs) ----
    "src/workflows/technical/graph.py": """\
class TechnicalGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【技術基準スタブ】入力: {q}"}

technical_graph = TechnicalGraphStub()
""",

    "src/workflows/failure/graph.py": """\
class FailureGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【不具合解析スタブ】入力: {q}"}

failure_graph = FailureGraphStub()
""",

    "src/workflows/law/graph.py": """\
class LawGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【法制度説明スタブ】入力: {q}"}

law_graph = LawGraphStub()
""",

    "src/workflows/pdf/graph.py": """\
class PdfGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【PDF解析スタブ】入力: {q}"}

pdf_graph = PdfGraphStub()
""",

    "src/workflows/general/graph.py": """\
class GeneralGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【通常QAスタブ】入力: {q}"}

general_graph = GeneralGraphStub()
""",

    # ---- UI Components ----
    "ui/components/chat_display.py": """\
import streamlit as st

def render_chat(messages):
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
""",

    "ui/components/chat_input.py": """\
import streamlit as st

def render_input_box():
    return st.chat_input("メッセージを入力してください")
""",
}

# -----------------------------
# 実行処理
# -----------------------------
def create_structure():
    print("📁 プロジェクト構成を生成中...\n")

    # Create folders
    for folder in FOLDERS:
        os.makedirs(folder, exist_ok=True)
        print(f"  ✔ フォルダ作成: {folder}")

    # Create files
    for path, content in FILES.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✔ ファイル作成: {path}")

    print("\n🎉 完成！プロジェクト構成が生成されました。")
    print("➡ app.py の中身に ChatGPT が生成した完成版 app.py を貼り付けてください。")


if __name__ == "__main__":
    create_structure()