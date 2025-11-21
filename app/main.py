from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_rag import router as rag_router
from app.api.routes_health import router as health_router

app = FastAPI(title="RAG Microservice")

# CORS básico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(health_router)
app.include_router(rag_router)
