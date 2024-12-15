from pydantic import BaseModel

class WolframRequestDto(BaseModel):
    input: str
    format: str
    output: str
    appid: str