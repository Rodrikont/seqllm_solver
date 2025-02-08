from pydantic import BaseModel
from models.usecase_equation_response import UsecaseEquationResponse

class ServerEquationResponse(BaseModel):
    status: int
    data: UsecaseEquationResponse
