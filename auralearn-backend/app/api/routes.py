from fastapi import APIRouter
from app.aws.kb_client import KnowledgeBaseClient

from app.agents.orchestrator import OrchestratorAgent

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/orchestrate")
def orchestrate(user_input: str):
    orchestrator = OrchestratorAgent()
    return orchestrator.execute(user_input)

@router.get("/test-kb")
def test_kb(query: str):
    kb = KnowledgeBaseClient()
    results = kb.search(query)
    return {
        "query": query,
        "results": results
    }
