from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Any, Dict
from .nodes import (
    node_route,
    node_retrieve,
    node_group,
    node_process_clauses,
    node_aggregate
)


class GraphState(TypedDict):
    input_text: str
    input_type: str
    rag_docs: List[Any]
    grouped_articles: List[Dict[str, Any]]
    clause_results: List[Dict[str, Any]]
    final_result: Dict[str, Any]


def build_judgement_graph():
    graph = StateGraph(GraphState)

    graph.add_node("route", node_route)
    graph.add_node("retrieve", node_retrieve)
    graph.add_node("group", node_group)
    graph.add_node("process", node_process_clauses)
    graph.add_node("aggregate", node_aggregate)

    graph.set_entry_point("route")
    graph.add_edge("route", "retrieve")
    graph.add_edge("retrieve", "group")
    graph.add_edge("group", "process")
    graph.add_edge("process", "aggregate")
    graph.add_edge("aggregate", END)

    return graph.compile()
