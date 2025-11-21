from typing import List, Dict, Any

def build_context_from_persons(persons: List[Dict[str, Any]]) -> str:
    """
    Construye un contexto textual legible para el LLM basado en la lista de personas.
    """
    if not persons:
        return "No hay personas registradas en el sistema."

    lines = []
    for p in persons:
        nombre = f"{p.get('primer_nombre', '')} {p.get('segundo_nombre', '')} {p.get('apellidos', '')}".strip()
        doc = f"{p.get('tipo_documento', '')} {p.get('nro_documento', '')}".strip()
        correo = p.get("correo", "")
        foto = p.get("foto", "Sin foto")

        line = f"Nombre: {nombre} | Documento: {doc} | Correo: {correo} | Foto: {foto}"
        lines.append(line)

    return "\n".join(lines)
