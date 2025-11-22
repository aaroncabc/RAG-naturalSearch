import httpx
from app.rag.config import GEMINI_API_URL, GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TIMEOUT
from app.rag.utils import logger
from app.rag.utils import extract_final_answer


async def call_huggingface(prompt: str, context: str):
    """
    Cliente para HF Router (formato OpenAI chat/completions).
    """
    if not GEMINI_API_URL or not GEMINI_API_KEY:
        return {"answer": None, "raw": None, "error": "Router no configurado"}

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GEMINI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Responde de manera breve y directa. "
                    "No incluyas razonamiento interno, ni etiquetas <think>, "
                    "Siempre que se encuentre una posible respuesta detente y retornala, necesitas garantizar la velocidad"
                )
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.2
    }


    async with httpx.AsyncClient(timeout=GEMINI_TIMEOUT) as client:
        try:
            resp = await client.post(GEMINI_API_URL, json=payload, headers=headers)
            data = resp.json()
        except Exception as e:
            logger.exception("Error llamando al router HF: %s", e)
            return {"answer": None, "raw": None, "error": str(e)}

    # Formato compatible con OpenAI
    try:
        raw_answer = data["choices"][0]["message"]["content"]
        answer = extract_final_answer(raw_answer)

    except Exception:
        answer = str(data)

    return {"answer": answer, "raw": data}
