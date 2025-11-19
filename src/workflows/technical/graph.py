class TechnicalGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【技術基準スタブ】入力: {q}"}

technical_graph = TechnicalGraphStub()
