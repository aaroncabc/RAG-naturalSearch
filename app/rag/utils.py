import logging
import json
import re

def extract_final_answer(text: str) -> str:
    """
    Elimina contenido <think>...</think> y devuelve solo la respuesta final.
    Funciona para DeepSeek-R1 y modelos similares.
    """
    if not text:
        return text

    # Eliminar bloques <think> ... </think>
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # Si sigue quedando algo antes de la respuesta final, limpiar
    return text.strip()


logger = logging.getLogger("rag-service")

def safe_json(obj):
    """Convierte un objeto a JSON seguro para logs."""
    try:
        return json.dumps(obj, ensure_ascii=False)[:1000]
    except:
        return str(obj)

def trim_text(text: str, max_len: int = 5000) -> str:
    """Evita enviar contexto extremadamente largo al LLM."""
    if text is None:
        return ""
    return text if len(text) <= max_len else text[:max_len] + "...[truncated]"

def normalize_string(s: str) -> str:
    if not s:
        return ""
    return str(s).strip()
