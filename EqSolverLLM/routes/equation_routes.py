from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from handlers.equation_handler import EquationHandler
from models.equation_request import EquationRequest
router_e = APIRouter()

# Обработчик для обработки вопросов
@router_e.post("/equation/")
async def solve_equation(dataReq: EquationRequest):
    try:
        resp = EquationHandler().execute(dataReq)
        if resp.status == "success":
            return JSONResponse(status_code=200, content=resp.dict(exclude_none=True))
        else:
            return JSONResponse(status_code=404, content=resp.dict(exclude_none=True)) 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))