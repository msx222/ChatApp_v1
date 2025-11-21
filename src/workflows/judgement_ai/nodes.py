from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from .dummy_rag import dummy_search_law, group_by_article
from .schema import FinalResult, ClauseResult, RequirementJudgement

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# 1) ルーティング（仕様書 or 不具合）
def node_route(state):
    text = state["input_text"]
    res = "spec" if "cd" in text or "光" in text else "failure"
    state["input_type"] = res
    return state


# 2) ダミーRAG
def node_retrieve(state):
    docs = dummy_search_law(state["input_text"])
    state["rag_docs"] = docs
    return state


# 3) 条文階層構造へ
def node_group(state):
    grouped = group_by_article(state["rag_docs"])
    state["grouped_articles"] = grouped
    return state


# 4) 各項を LLM で判定する
def process_clause(user_text, article, clause, clause_text):
    prompt = f"""
ユーザー入力: {user_text}
条文（{article} {clause}）:
{clause_text}

要求要件を箇条書きで抽出し、各要件が適合かどうかを判定し、JSONで返してください。
"""
    res = llm.invoke(prompt).content
    # 本来は JSON パーシング
    # 今はダミー：
    return {
        "article": article,
        "article_title": "",
        "clause": clause,
        "overall": "不適合",
        "requirements": [
            {
                "req_id": "R1",
                "text": clause_text,
                "judgement": "不適合",
                "confidence": 1.0,
                "reasoning": "ダミー判定"
            }
        ]
    }


def node_process_clauses(state):
    results = []
    for art in state["grouped_articles"]:
        article = art["article"]
        for cl in art["clauses"]:
            clause_name = cl["clause"]
            clause_text = "\n".join(d.page_content for d in cl["chunks"])
            r = process_clause(
                user_text=state["input_text"],
                article=article,
                clause=clause_name,
                clause_text=clause_text,
            )
            results.append(r)
    state["clause_results"] = results
    return state


# 5) 集約
def node_aggregate(state):
    clause_results = state["clause_results"]
    articles_map = {}

    for c in clause_results:
        art = c["article"]
        if art not in articles_map:
            articles_map[art] = {"article": art, "title": "", "clauses": []}
        articles_map[art]["clauses"].append({
            "clause": c["clause"],
            "overall": c["overall"],
            "requirements": c["requirements"]
        })

    final = FinalResult(
        overall_judgement="不適合",
        reasoning="ダミー集計",
        advice="改善してください",
        articles=list(articles_map.values()),
        clause_results=[]
    )

    state["final_result"] = final.dict()
    return state
