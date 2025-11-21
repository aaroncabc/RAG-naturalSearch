from pydantic import BaseModel

class QueryBody(BaseModel):
    consulta: str
