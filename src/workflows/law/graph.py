class LawGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【法制度説明スタブ】入力: {q}"}

law_graph = LawGraphStub()
