from clients import llm_clients
from config.config import config
from models.usecase_equation_response import UsecaseEquationResponse
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from settings import settings

class EquationUseCase:
    def __init__(self):
        self.config = config

    def equation(self, equation: str) -> UsecaseEquationResponse:
        cResp = self.send_qwen(equation)

        if cResp.answer == "True" :
            cResp = self.send_wolfam(equation)
            resp = UsecaseEquationResponse(
                answer=cResp.answer,
                error=cResp.error
            )
        else:
            print("error while Qwen check")
            resp = UsecaseEquationResponse(
                answer = "error",
                error = 'Error while Qwen check'
                )

        return resp

    def send_qwen(self, equation: str) -> UsecaseEquationResponse:
        a = False
        for i in range(self.config.client_qwen.cycle_count):
            dataReq = ClientEquationRequest(
                question=f"{equation}\n{settings.REQUESTS_TO_QWEN[i]}",
                )

            cResp = llm_clients.NewLlmClient(llm_clients.LlmClientsType.QWEN).ask_question(dataReq)

            answer = "True"
            if not cResp.answer == 'Да' and i in (1, 2):
                answer = "False"
            if cResp.answer == 'Да' and i == 3:
                answer = "False"
            if cResp.answer == 'Да' and i in (4, 5, 6):
                a = True
        if a == True:
            answer = "True"
        
        resp = UsecaseEquationResponse(answer=answer)

        return resp
            
    def send_wolfam(self, question: str) -> ClientEquationResponse:
        req = ClientEquationRequest(question=question)
        resp = llm_clients.NewLlmClient(llm_clients.LlmClientsType.WOLFRAM).ask_question(req)
        print(resp)
        return resp
