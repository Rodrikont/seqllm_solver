from pydantic import BaseModel
from typing import Optional

class EquationDataResponse(BaseModel):
    answer: str
    error: Optional[str] = None
