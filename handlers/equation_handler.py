from handlers.handler_interface import HandlerInterface
from usecases.equation_usecase import EquationUseCase
from models.server_equation_request import ServerEquationRequest
from models.server_equation_response import ServerEquationResponse
from settings import settings

class EquationHandler(HandlerInterface):
    def __init__(self):
        return

    # Ne nado bolshe
    '''    
    def convert(data):
        b = ''
        for i in range(len(data)):
            if data[i] in settings.SYMBOLS:
                b += settings.SYMBOLS[data[i]]
            else:
                b += data[i]
        return b
    '''

    def execute(self, dataReq: ServerEquationRequest) -> ServerEquationResponse:
        print(f"Handling data: {dataReq}")

        uResp = EquationUseCase().equation(dataReq.question)

        resp = ServerEquationResponse(
            status = 200,
            data = uResp
        )

        if uResp.error is not None:
            resp.status = uResp.status
            resp.message = uResp.error
            resp.data = uResp

        else:
            resp.message = uResp.answer


        return resp

