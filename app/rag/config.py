import os

# Microservicio de personas
PERSONS_SERVICE_URL = os.getenv("PERSONS_SERVICE_URL", "http://localhost:3002/persons")
PERSONS_TIMEOUT = float(os.getenv("PERSONS_TIMEOUT", "8.0"))

# Gemini API
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_TIMEOUT = float(os.getenv("GEMINI_TIMEOUT", "20.0"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# Otros
MAX_CONTEXT_PERSONS = int(os.getenv("MAX_CONTEXT_PERSONS", "12"))
LOG_LLM_RESPONSES = os.getenv("LOG_LLM_RESPONSES", "true").lower() == "true"
