from typing import Dict, Any, List
from app.rag.persons_client import fetch_persons
from app.rag.mapper import map_person_from_api
from app.rag.context_builder import build_context_from_persons
from app.rag.llm_client import call_gemini
from app.rag.config import MAX_CONTEXT_PERSONS
from app.rag.utils import logger


async def rag_process(consulta: str) -> List[Dict[str, Any]]:
    """
    Lógica principal del endpoint /rag usado por el frontend.
    Debe devolver SOLO la lista de personas.
    """
    logger.info("Ejecutando RAG para consulta: %s", consulta)

    # 1. Obtener personas del microservicio
    persons_raw = await fetch_persons()

    # 2. Mapear personas al formato usado por el frontend
    mapped = [map_person_from_api(p) for p in persons_raw]

    # Si no hay resultados, devolver lista vacía (frontend lo maneja)
    if not mapped:
        return []

    # 3. Construir contexto
    context = build_context_from_persons(mapped[:MAX_CONTEXT_PERSONS])

    # 4. Llamar al LLM (no afecta la respuesta enviada al frontend)
    await call_gemini(consulta, context)

    # 5. Devolver SOLO la lista mapeada (frontend usa personas)
    return mapped


async def rag_full_process(consulta: str) -> Dict[str, Any]:
    """
    Devuelve: personas + respuesta del LLM.
    Perfecto para debugging o endpoints internos.
    """
    persons_raw = await fetch_persons()
    mapped = [map_person_from_api(p) for p in persons_raw]

    context = build_context_from_persons(mapped[:MAX_CONTEXT_PERSONS])
    llm = await call_gemini(consulta, context)

    return {
        "personas": mapped,
        "answer": llm.get("answer"),
        "raw": llm.get("raw")
    }
