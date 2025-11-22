from fastapi import APIRouter, HTTPException
from app.models.request_models import QueryBody
from app.rag.service import rag_process, rag_full_process

router = APIRouter()

@router.post("/rag")
async def rag_endpoint(body: QueryBody):
    """
    Endpoint usado por el frontend.
    Solo devuelve la lista mapeada de personas.
    """
    try:
        personas = await rag_process(body.consulta)
        return personas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag_full")
async def rag_full_endpoint(body: QueryBody):
    """
    Endpoint de debugging: personas + respuesta del modelo Gemini.
    Úsalo para validar que todo el pipeline funciona.
    """
    try:
        resultado = await rag_full_process(body.consulta)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
