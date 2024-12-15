from fastapi import APIRouter, HTTPException
from SEULLM.EqSolverLLM.handlers.del_wolfram_handler import Wolfram_Handler

router_w = APIRouter()

# Обработчик для 
@router_w.post("/wolfram/")
async def request_to_wolfram(dataReq: dict):
    try:
        result = Wolfram_Handler().answer(dataReq)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))