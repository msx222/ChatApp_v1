from pydantic import BaseModel
from typing import List, Dict, Any


class RequirementJudgement(BaseModel):
    req_id: str
    text: str
    judgement: str
    confidence: float
    reasoning: str


class ClauseResult(BaseModel):
    article: str
    article_title: str
    clause: str
    overall: str
    requirements: List[RequirementJudgement]


class FinalResult(BaseModel):
    overall_judgement: str
    reasoning: str
    advice: str
    articles: List[Dict[str, Any]]
    clause_results: List[ClauseResult]
