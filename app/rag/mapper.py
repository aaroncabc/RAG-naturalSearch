from typing import Dict, Any
from rag.utils import normalize_string


def map_person_from_api(p: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mapea la estructura del backend al formato del frontend.
    Si vienen nombres distintos, este mapper los normaliza.
    """
    return {
        "primer_nombre": normalize_string(
            p.get("primer_nombre") or
            p.get("first_name")
        ),
        "segundo_nombre": normalize_string(
            p.get("segundo_nombre") or
            p.get("middle_name")
        ),
        "apellidos": normalize_string(
            p.get("apellidos") or
            p.get("last_name")
        ),
        "tipo_documento": normalize_string(
            p.get("tipo_documento") or
            p.get("doc_type")
        ),
        "nro_documento": normalize_string(
            p.get("nro_documento") or
            p.get("document_number") or
            p.get("nroDocumento")
        ),
        "correo": normalize_string(
            p.get("correo") or
            p.get("email")
        ),
        "foto": p.get("foto") or p.get("photo") or None,
    }
