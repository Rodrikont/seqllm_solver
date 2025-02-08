from typing import Optional, Dict, Any
from enums.status_enums import Status
from dataclasses import dataclass, field, asdict

@dataclass
class UsecaseEquationResponse:
    status: str | None = Status.NONE.value
    roots: list = field(default_factory=list)
    aproxRoots: list = field(default_factory=list)
    answer: Optional[str] = None
    error: Optional[str] = None
