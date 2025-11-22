import httpx
from app.rag.config import GEMINI_API_URL, GEMINI_API_KEY, GEMINI_TIMEOUT
from app.rag.utils import logger, safe_json


async def call_gemini(prompt: str, context: str):
    """
    Cliente compatible con Google Gemini API (Google AI Studio).
    Usa generateContent y API Key en query param.
    """

    if not GEMINI_API_URL or not GEMINI_API_KEY:
        logger.warning("Gemini no configurado.")
        return {"answer": None, "raw": None, "error": "Gemini no configurado"}

    # URL final de la API
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

    # Estructura OFICIAL de Google AI Studio
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Contexto:\n{context}\n\nPregunta:\n{prompt}"
                    }
                ]
            }
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=GEMINI_TIMEOUT) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()

    except Exception as e:
        logger.exception("Error llamando a Gemini: %s", e)
        return {"answer": None, "raw": None, "error": str(e)}

    # Si hay error HTTP
    if resp.status_code != 200:
        logger.error("Error Gemini: %s", data)
        return {"answer": None, "raw": data, "error": "Gemini error"}

    # Extraer respuesta
    try:
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        answer = None

    logger.info("Respuesta LLM: %s", safe_json(answer))
    return {
        "answer": answer,
        "raw": data
    }
