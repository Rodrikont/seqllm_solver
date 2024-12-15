from pydantic import BaseModel
from typing import List

class QwenRequestDto(BaseModel):
    query: str
    history: List[str]
    system: str
    api_name: str