class PdfGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【PDF解析スタブ】入力: {q}"}

pdf_graph = PdfGraphStub()
