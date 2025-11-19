def classify_query(text: str):
    """スタブ版のルーター：簡易キーワード分類"""
    if "振動" in text or "異音" in text:
        return {"workflow": "failure"}
    if "条文" in text or "法" in text:
        return {"workflow": "law"}
    if "PDF" in text:
        return {"workflow": "pdf"}
    if "基準" in text or "寸法" in text:
        return {"workflow": "technical"}

    return {"workflow": "general"}
