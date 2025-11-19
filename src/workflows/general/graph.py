class GeneralGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【通常QAスタブ】入力: {q}"}

general_graph = GeneralGraphStub()
