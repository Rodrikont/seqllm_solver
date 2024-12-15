from handlers.handler_interface import HandlerInterface
from usecases.equation_usecase import EquationUseCase
from models.equation_request import EquationRequest
from models.equation_data_response import EquationDataResponse
from models.equation_response import EquationResponse
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

    def execute(self, dataReq: EquationRequest):
        print(f"Handling data: {dataReq}")

        dataResp: EquationDataResponse = EquationUseCase().equation(dataReq.question)

        resp = EquationResponse(
            status = "success",
            data = dataResp
        )

        if dataResp.error is not None:
            resp.status = "error"
            resp.message = dataResp.error
            resp.data = None


        return resp

