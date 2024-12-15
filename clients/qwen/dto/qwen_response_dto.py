from pydantic import BaseModel

class QwenResponseDto(BaseModel):
    temp: str
