from gradio_client import Client
from settings import settings
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from clients.qwen.dto.qwen_request_dto import QwenRequestDto
from clients.qwen.dto.qwen_response_dto import QwenResponseDto
from enums.status_enums import Status

client = Client("Qwen/Qwen2.5-72B-Instruct")

class QwenClient:
    def ask_question(self, data: ClientEquationRequest) -> ClientEquationResponse:
        try:
            result = client.predict(
                query=data.question,
                history=[],
                system="You are Qwen, created by Alibaba Cloud. You are a helpful assistant.",
                api_name="/model_chat"
            )
            '''req = QwenRequestDto(
                query=data.question,
                history=[],
                system="You are Qwen, created by Alibaba Cloud. You are a helpful assistant.",
                api_name="/model_chat"
            )

            result = client.predict(req.dict())
            '''

            # resp = QwenResponseDto(**result)

            print(f"{data.question}") # log
            print(f"Ответ: {result[-2][0][-1]}") # log
            print()

            resp = ClientEquationResponse(
                answer=result[-2][0][-1],
            )
        except Exception as e:
            print(e)
            return ClientEquationResponse(
                status=Status.ERROR.value,
                error=f"Ошибка: {e}",
            )

        return resp