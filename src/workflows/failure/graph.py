class FailureGraphStub:
    def invoke(self, state: dict):
        q = state["user_query"]
        return {"answer": f"【不具合解析スタブ】入力: {q}"}

failure_graph = FailureGraphStub()
