from fastapi import APIRouter
from app.models.request_models import QueryBody

router = APIRouter()

@router.post("/rag")
def rag_endpoint(body: QueryBody):
    return {
        "message": "RAG endpoint listo",
        "consulta": body.consulta
    }
