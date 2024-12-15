from pydantic import BaseModel

class EquationRequest(BaseModel):
    question: str
