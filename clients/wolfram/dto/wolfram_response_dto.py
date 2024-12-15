from pydantic import BaseModel

class WolframResponseDto(BaseModel):
    queryresult: dict
