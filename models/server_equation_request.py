from pydantic import BaseModel
from typing import Optional
from dataclasses import dataclass

@dataclass
class ServerEquationRequest(BaseModel):
    question: str
