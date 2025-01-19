from typing import Optional
from dataclasses import dataclass

@dataclass
class UsecaseEquationResponse:
    answer: str
    answer2: str | None = None
    sol_count: int | None = 1
    status: int | None = 200
    error: Optional[str] = None
