# 📝 **README – Servicio RAG con HuggingFace Router**

## 📌 **Descripción del Proyecto**

Este servicio implementa un **sistema RAG (Retrieval-Augmented Generation)** que:

- Consulta un microservicio externo para obtener personas (opcional).
- Procesa una pregunta del usuario.
- Llama a un modelo LLM a través del **HuggingFace Inference Router**.
- Retorna una respuesta generada por el modelo, usando modo sin pensamiento interno cuando es compatible.

Diseñado para ser **simple**, **modular**, fácil de contenerizar en **Docker**, y usable en proyectos académicos o demostrativos sin necesidad de proveedores con billing activo.

---

## 🚀 **Endpoints Principales**

### **GET /check_llm**
Prueba simple para verificar la conexión con el modelo LLM.


Ejemplo de petición:

```json
{
  "consulta": "¿Qué fecha es hoy?"
}
```

Ejemplo de respuesta:

```json
{
  "personas": [],
  "answer": "28 de marzo de 2025",
  "raw": {...}
}
```


## 🔹 **POST /rag**

### **Descripción**
Endpoint principal usado por el **frontend**.  
Procesa la consulta del usuario, obtiene los datos del microservicio de personas y devuelve **solo la lista mapeada**, lista para ser consumida por React.

### **Body esperado**
```json
{
  "consulta": "texto de la consulta"
}
```

### **Respuesta**
Lista de personas mapeadas:

```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "edad": 30
  }
]
```

Si no hay personas:

```json
[]
```

### **Errores**
- `500` error interno si falla el RAG o el microservicio.

---

## 🔹 **POST /rag_full**

### **Descripción**
Endpoint completo de depuración (**solo para pruebas**).  
Devuelve:

- Personas obtenidas  
- Respuesta final del LLM  
- Respuesta cruda del proveedor (HuggingFace Router)

Sirve para verificar que el modelo está respondiendo correctamente, que el pipeline está funcionando y que la integración con HuggingFace Router es correcta.

### **Body esperado**
```json
{
  "consulta": "texto de la consulta"
}
```

### **Respuesta**
```json
{
  "personas": [
    { "id": 1, "nombre": "Juan Pérez" }
  ],
  "answer": "La respuesta procesada del modelo",
  "raw": { ... respuesta original del modelo ... }
}
```

### **Errores**
- `500` si algún componente del pipeline falla.

---

## 📝 Notas adicionales

- `/rag` debe ser usado por el frontend en producción.
- `/rag_full` es solo para desarrolladores (debug).
- Ambos endpoints esperan el mismo modelo `QueryBody`.

---

## 🛠 **Requisitos**

- Docker
- Archivo `.env` ubicado en la raíz del proyecto

---

# 📦 **Instrucciones de Docker**

## 🔨 **1. Construir la imagen**

```bash
docker build -t servicio-rag .
```

## ▶️ **2. Ejecutar el contenedor con variables de entorno**

```bash
docker run --env-file .env -p 8000:8000 servicio-rag
```

Esto levantará el servicio en:

👉 http://localhost:8000  
👉 http://localhost:8000/docs

---

# 🧩 **Formato del archivo `.env`**

```
# URL del microservicio de personas (opcional)
PERSONS_API_URL=http://localhost:3001/persons

# Router de HuggingFace (API unificada)
GEMINI_API_URL=https://router.huggingface.co/v1/chat/completions
GEMINI_API_KEY=tu_token_de_huggingface

# Modelo a usar
GEMINI_MODEL=google/gemma-2-27b-it

# Timeout en segundos
GEMINI_TIMEOUT=30
```

---

# 📁 **Estructura del Proyecto (resumen)**

```
app/
 ├── api/
 │    ├── routes_rag.py
 ├── rag/
 │    ├── service.py
 │    ├── llm_client.py
 │    ├── persons_client.py
 │    ├── config.py
 │    └── utils.py
 ├── main.py
Dockerfile
.env
README.txt
```

---

# 🧪 **Prueba rápida**

```
curl http://localhost:8000/check_llm
```

o vía navegador:

👉 http://localhost:8000/docs

---

# 🤝 **Soporte**

Si deseas agregar nuevas fuentes de datos o cambiar de modelo, puedo ayudarte con la extensión del proyecto.
