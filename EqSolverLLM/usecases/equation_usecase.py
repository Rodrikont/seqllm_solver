from clients import qwen_client
from config.config import config
from models.equation_data_response import EquationDataResponse
from clients.wolfram_client import WolframClient
# from settings import settings

class EquationUseCase:
    def __init__(self):
        self.config = config

    def equation(self, question: str) -> EquationDataResponse:
        if EquationUseCase.send_qwen(self, question):
            resp = EquationDataResponse(
                answer = EquationUseCase.send_wolfam(self, question)
            )
        else:
            resp = EquationDataResponse(
                answer = "error",
                error = 'Not Equation'
            )
        return resp

    def send_qwen(self, dataReq):
        a = False
        for i in range(1, self.config.client_qwen.cycle_count + 1):
            answ = qwen_client.Qwen.reqwest_llm(dataReq, i)
#             print(answ) # log
            if not answ == 'Да' and i in (1, 2):
                return False
            if answ == 'Да' and i == 3:
                return False
            if answ == 'Да' and i in (4, 5, 6):
                a = True
        if a == True:
            return True
            
    def send_wolfam(self, dataReq):
        answer: EquationDataResponse = WolframClient.request(dataReq)
        return answer
