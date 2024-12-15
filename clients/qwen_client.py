from gradio_client import Client
from settings import settings

client = Client("Qwen/Qwen2.5-72B-Instruct")

class Qwen:
    def reqwest_llm(inp, req_num):
        result = client.predict(
            query=f"{inp}\n" + settings.REQUESTS_TO_QWEN[req_num - 1],
            history=[],
            system="You are Qwen, created by Alibaba Cloud. You are a helpful assistant.",
            api_name="/model_chat"
        )
        print(result[-2][0][-1]) # log
        return result[-2][0][-1]