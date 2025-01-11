from typing import Optional
from dataclasses import dataclass

@dataclass
class UsecaseEquationResponse:
    answer: str
    status: int | None = 200
    error: Optional[str] = None
