import httpx
from rag.config import GEMINI_API_URL, GEMINI_API_KEY, GEMINI_TIMEOUT, GEMINI_MODEL
from rag.utils import logger, safe_json


async def call_gemini(prompt: str, context: str):
    """
    Llama a la API de Gemini. El formato es flexible para adaptarse a varias implementaciones.
    """
    if not GEMINI_API_URL or not GEMINI_API_KEY:
        logger.warning("Gemini no está configurado (GEMINI_API_URL/GEMINI_API_KEY).")
        return {"answer": None, "raw": None, "error": "Gemini no configurado"}

    payload = {
        "model": GEMINI_MODEL,
        "prompt": f"Contexto:\n{context}\n\nPregunta:\n{prompt}",
        "max_tokens": 300,
        "temperature": 0.0,
    }

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=GEMINI_TIMEOUT) as client:
        try:
            resp = await client.post(GEMINI_API_URL, json=payload, headers=headers)
        except Exception as e:
            logger.exception("Error llamando a Gemini: %s", e)
            return {"answer": None, "raw": None, "error": str(e)}

        # Parse flexible (diferentes APIs dan diferentes estructuras)
        try:
            data = resp.json()
        except Exception:
            return {"answer": None, "raw": resp.text, "error": "JSON inválido"}

        answer = None

        if isinstance(data, dict):
            answer = (
                data.get("output") or
                data.get("output_text") or
                (data.get("choices") or [{}])[0].get("text") or
                (data.get("candidates") or [{}])[0].get("content")
            )

        answer = answer or str(data)

        logger.info("Respuesta LLM: %s", safe_json(answer))
        return {"answer": answer, "raw": data}
