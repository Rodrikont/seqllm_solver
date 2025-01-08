from handlers.del_wolfram_handler import WolframHandler
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from clients.wolfram.dto.wolfram_request_dto import WolframRequestDto
from clients.wolfram.dto.wolfram_response_dto import WolframResponseDto
from settings import settings
import requests

class WolframClient:
    def ask_question(self, data: ClientEquationRequest) -> ClientEquationResponse:
        try:
            req = WolframRequestDto(
                 input = data.question,
                 format = 'plaintext',
                 output = 'JSON',
                 appid = 'VTPUR2-T2TER673J7'
            )

            dReq = req.dict()

            response = requests.post(settings.WOLFRAM_URL, data=dReq)
            #response.raise_for_status()

            if response.status_code == 200:
                # Преобразуем ответ в структуру (объект Pydantic)
                try:
                    # Проверка статуса запроса
                    response.raise_for_status()
                    # Получаем JSON из ответа
                    jsonResp = response.json() 
                    # Преобразуем в структуру
                    respDto = WolframResponseDto.parse_obj(jsonResp) 
                except ValueError as e:                    
                    print(f"Ошибка разбора JSON: {e}")
                except Exception as e:
                    print(e)
                    return ClientEquationResponse(error=f"Ошибка преобразования ответа: {e}")
            else:
                print(f"Ошибка запроса: {response.status_code}")
                return ClientEquationResponse(error=f"Ошибка запроса: {response.status_code}")

            # print(response_data) # uravnenie nado bylo
            var: str = ""
            if respDto is not None:
                        qResult  = respDto.queryresult
                        if qResult is not None :
                            pods = qResult.get("pods")
                            for pod in pods:
                                if pod.get('title') == "Solution" or pod.get('title') == "Solutions":
                                    subpods = pod.get('subpods')
                                    for subpod in subpods: 
                                        if var != "":
                                             var += "; "
                                        var += subpod.get('plaintext')
                                        # Debug
                                        print(var)
            else:
                 print("Модель не отвечает")
                 return ClientEquationResponse(error="Модель не отвечает")
            answer = var
        except requests.exceptions.RequestException as e:
            print(e)
            return ClientEquationResponse(error=f"Ошибка запроса: {e}")
        except ValueError:
            print(e)
            return ClientEquationResponse(error="Не удалось преобразовать ответ")

        cResp = ClientEquationResponse(answer=answer)

        return cResp
    
if __name__ == '__main__':
    print(WolframClient.request(''))