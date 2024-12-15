from pydantic import BaseModel
from models.equation_data_response import EquationDataResponse

class EquationResponse(BaseModel):
    status: str
    message: str = ""
    data: EquationDataResponse
