from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class ServerEquationRequest(BaseModel):
    question: str
