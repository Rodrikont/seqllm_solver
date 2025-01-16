from pydantic import BaseModel
from models.usecase_equation_response import UsecaseEquationResponse

class ServerEquationResponse(BaseModel):
    status: int | None = 200
    message: list = [None, None]
    data: UsecaseEquationResponse
