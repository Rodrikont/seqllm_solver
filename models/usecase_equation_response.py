from typing import Optional
from dataclasses import dataclass

@dataclass
class UsecaseEquationResponse:
    answer: str
    error: Optional[str] = None
