from pydantic import BaseModel

class ServerEquationRequest(BaseModel):
    question: str
