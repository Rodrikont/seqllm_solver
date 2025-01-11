from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from handlers.equation_handler import EquationHandler
from models.server_equation_request import ServerEquationRequest
router_e = APIRouter()

# Обработчик для обработки вопросов
@router_e.post("/equation/")
async def solve_equation(dataReq: ServerEquationRequest):
    try:
        resp = EquationHandler().execute(dataReq)
        if resp.status == 200:
            return JSONResponse(status_code=200, content=resp.dict(exclude_none=True))
        else:
            print(404)
            return JSONResponse(status_code=404, content=resp.dict(exclude_none=True)) 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))