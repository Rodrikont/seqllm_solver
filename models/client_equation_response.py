from typing import Optional
from dataclasses import dataclass

@dataclass
class ClientEquationResponse:
    answer: Optional[str] = None
    status: int | None = 200
    error: Optional[str] = None