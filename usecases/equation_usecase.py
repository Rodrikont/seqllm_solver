from clients import llm_clients
from config.config import config
from models.usecase_equation_response import UsecaseEquationResponse
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from settings import settings
from enums.status_enums import Status

class EquationUseCase:
    def __init__(self):
        self.config = config

    def equation(self, equation: str) -> UsecaseEquationResponse:
        cResp = self.send_qwen(equation)

        if cResp.answer == "True" :
            cResp = self.send_wolfam(equation)
            resp = UsecaseEquationResponse(
                answer=cResp.answer,
                roots=cResp.roots,
                aproxRoots=cResp.aproxRoots,
                status=cResp.status,
                error=cResp.error
            )
        else:
            print("error while Qwen check")
            resp = UsecaseEquationResponse(
                status=Status.ERROR.value,
                error='Error while Qwen check'
                )

        return resp

    def send_qwen(self, equation: str) -> UsecaseEquationResponse:
        isRight = True

        for q in settings.REQUESTS_REQUIRED_TO_QWEN:
            dataReq = ClientEquationRequest(
                question=f"{equation}{q}",
                )

            cResp = llm_clients.NewLlmClient(llm_clients.LlmClientsType.QWEN).ask_question(dataReq)

            if cResp.answer == 'Нет':
                isRight = False
                break

        if isRight == True:
            isRight = False
            for q in settings.REQUESTS_CONSISTENT_TO_QWEN:
                dataReq = ClientEquationRequest(
                    question=f"{equation}{q}",
                    )

                cResp = llm_clients.NewLlmClient(llm_clients.LlmClientsType.QWEN).ask_question(dataReq)

                if cResp.answer == 'Да':
                    isRight = True
                    break

        answer = "False"
        if isRight == True:
            answer = "True"
        
        resp = UsecaseEquationResponse(answer=answer)

        return resp
            
    def send_wolfam(self, question: str) -> ClientEquationResponse:
        req = ClientEquationRequest(question=question)
        resp = llm_clients.NewLlmClient(llm_clients.LlmClientsType.WOLFRAM).ask_question(req)
        print(resp)
        return resp
