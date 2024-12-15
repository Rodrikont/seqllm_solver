from gradio_client import Client
from settings import settings
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from clients.qwen.dto.qwen_request_dto import QwenRequestDto
from clients.qwen.dto.qwen_response_dto import QwenResponseDto

client = Client("Qwen/Qwen2.5-72B-Instruct")

class QwenClient:
    def ask_question(self, data: ClientEquationRequest) -> ClientEquationResponse:
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

        print(f"{result[-2][0][-1]} - {data.question}") # log

        resp = ClientEquationResponse(
            result[-2][0][-1],
        )

        return resp