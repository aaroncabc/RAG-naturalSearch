import httpx
from typing import List, Dict, Any
from app.rag.config import PERSONS_SERVICE_URL, PERSONS_TIMEOUT
from app.rag.utils import logger


async def fetch_persons() -> List[Dict[str, Any]]:
    """
    Llama al microservicio de personas EXACTAMENTE igual a como lo hace el frontend.
    Espera: { "data": [ ... ] }
    """
    logger.info("Consultando microservicio de personas: %s", PERSONS_SERVICE_URL)

    async with httpx.AsyncClient(timeout=PERSONS_TIMEOUT) as client:
        try:
            response = await client.get(PERSONS_SERVICE_URL)
        except Exception as e:
            logger.exception("Error conectando al microservicio de personas: %s", e)
            return []

        if response.status_code != 200:
            logger.warning("Microservicio de personas devolvió %s", response.status_code)
            return []

        try:
            raw = response.json()
            if isinstance(raw, dict) and "data" in raw and isinstance(raw["data"], list):
                return raw["data"]
            logger.warning("Formato inesperado en respuesta del microservicio de personas: %s", raw)
            return []
        except Exception as e:
            logger.exception("Error parseando JSON del microservicio de personas: %s", e)
            return []
