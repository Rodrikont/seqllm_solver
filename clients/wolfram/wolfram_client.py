from handlers.del_wolfram_handler import WolframHandler
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from clients.wolfram.dto.wolfram_request_dto import WolframRequestDto
from clients.wolfram.dto.wolfram_response_dto import WolframResponseDto
from config.config import config
from settings import settings
import requests

class WolframClient:
    def ask_question(self, data: ClientEquationRequest) -> ClientEquationResponse:
        try:
            req = WolframRequestDto(
                 input = data.question,
                 format = "plaintext",
                 output = "JSON",
                 appid = config.client_wolfram.appid
            )

            dReq = req.dict()

            print("REQUEST")
            print(dReq)

            response = requests.post(config.client_wolfram.url, data=dReq)
            #response.raise_for_status()

            if response.status_code == 200:
                # Преобразуем ответ в структуру (объект Pydantic)
                try:
                    # Проверка статуса запроса
                    response.raise_for_status()
                    # Получаем JSON из ответа
                    jsonResp = response.json()
                    print("RESPONSE")
                    print(jsonResp)
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
            vs = ["", ""]
            if respDto is not None:
                        qResult  = respDto.queryresult
                        if qResult is not None :
                            pods = qResult.get("pods")
                            for pod in pods:
                                if pod.get("title") == "Solution":
                                    sol_cnt = 1
                                    subpods = pod.get("subpods")
                                    vs[0] = subpods[0].get("plaintext")
                                    # Debug
                                    print(vs)
                                elif pod.get("title") == "Solutions":
                                    sol_cnt = 2
                                    subpods = pod.get("subpods")
                                    vs = []
                                    for subpod in subpods:
                                        vs.append(subpod.get("plaintext"))
                                    #Debug
                                    print(vs)
                                else:
                                    print("No solutions\n\n")
                                    print(pods)
                        else:
                            print("Empty answer")
            else:
                 print("Модель не отвечает")
                 return ClientEquationResponse(error="Модель не отвечает")
            answer = vs[0]
        except requests.exceptions.RequestException as e:
            print(e)
            return ClientEquationResponse(error=f"Ошибка запроса: {e}")
        except ValueError:
            print(e)
            return ClientEquationResponse(error="Не удалось преобразовать ответ")

        if sol_cnt == 2:
            cResp = ClientEquationResponse(answer=answer, answer2=vs[1], sol_count=sol_cnt)
        elif sol_cnt == 1:
            cResp = ClientEquationResponse(answer=answer)

        return cResp
    
if __name__ == "__main__":
    print(WolframClient.request(""))