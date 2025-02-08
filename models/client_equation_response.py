from typing import Optional
from enums.status_enums import Status
from dataclasses import dataclass, field

@dataclass
class ClientEquationResponse:
    status: str | None = Status.NONE.value
    roots: list = field(default_factory=list)
    aproxRoots: list = field(default_factory=list)
    answer: Optional[str] = None
    error: Optional[str] = None