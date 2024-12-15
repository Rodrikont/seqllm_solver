from typing import Optional
from dataclasses import dataclass

@dataclass
class ClientEquationResponse:
    answer: Optional[str] = None
    error: Optional[str] = None