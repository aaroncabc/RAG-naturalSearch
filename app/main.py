from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_rag import router as rag_router
from app.api.routes_health import router as health_router
from app.rag.llm_client import call_huggingface


app = FastAPI(title="RAG Microservice")

# CORS básico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/check_llm")
async def check_llm():
    try:
        respuesta = await call_huggingface("Hola Gemini, ¿qué fecha es hoy?", "")
        return respuesta
    except Exception as e:
        return {"error": str(e)}


# Registrar rutas
app.include_router(health_router)
app.include_router(rag_router)
