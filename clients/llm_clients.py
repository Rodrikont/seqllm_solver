from enum import Enum
from clients.qwen.qwen_client import QwenClient
from clients.wolfram.wolfram_client import WolframClient

class LlmClientsType(Enum):
    QWEN = 1
    WOLFRAM = 2

def NewLlmClient(client_type):
    if client_type == LlmClientsType.QWEN:
        return QwenClient()
    elif client_type == LlmClientsType.WOLFRAM:
        return WolframClient()
    else:
        raise ValueError("Unknown client type")