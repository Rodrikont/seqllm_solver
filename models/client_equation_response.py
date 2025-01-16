from typing import Optional
from dataclasses import dataclass

@dataclass
class ClientEquationResponse:
    answer: Optional[str] = None
    answer2: Optional[str] = None
    sol_count: int | None = 1
    status: int | None = 200
    error: Optional[str] = None