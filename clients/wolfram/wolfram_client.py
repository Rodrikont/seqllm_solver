'''from handlers.del_wolfram_handler import WolframHandler
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from clients.wolfram.dto.wolfram_request_dto import WolframRequestDto
from clients.wolfram.dto.wolfram_response_dto import WolframResponseDto
from config.config import config
from settings import settings
from sympy import sympify
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
            sol_cnt = 0
            if respDto is not None:
                        qResult  = respDto.queryresult
                        if qResult is not None and "pods" in qResult:
                            pods = qResult.get("pods")
                            for pod in pods:
                                if "title" in pod and "Solution" in pod["title"]:
                                    if "subpods" in pod:
                                        if "Solutions" in pod.get("title"):
                                            sol_cnt = 2
                                            subpods = pod.get("subpods")
                                            vs = []
                                            for subpod in subpods:
                                                vs.append(subpod.get("plaintext"))
                                            #Debug
                                            print(vs)
                                        else:
                                            sol_cnt = 1
                                            subpods = pod.get("subpods")
                                            vs[0] = subpods[0].get("plaintext")
                                            # Debug
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
        except ValueError as e:
            print(e)
            return ClientEquationResponse(error="Не удалось преобразовать ответ")

        cResp = None

        if sol_cnt == 2:
            try:
                x = sympify(answer)
                y = sympify(vs[1])
            except:
                print("Ошибка преобразования выражения")
                cResp = ClientEquationResponse(error="Ошибка преобразования выражения")
            try:
                if x != x.evalf() and y == y.evalf():
                    if x == x.evalf():
                        cResp = ClientEquationResponse(answer=answer, sol_count=sol_cnt)
                        cResp.answer2 = f"Точно: {y}\nПримерно: {y.evalf()}"
                    if y == y.evalf():
                        cResp = ClientEquationResponse(answer=f"Точно: {x}\nПримерно: {x.evalf()}", sol_count=sol_cnt)
                        cResp.answer2 = vs[1]
                else:
                    cResp = ClientEquationResponse(answer=answer, answer2=vs[1], sol_count=sol_cnt)
            except:
                cResp = ClientEquationResponse(error="Ошибка сборки ответа")
        elif sol_cnt == 1:
            try:
                x = sympify(answer)
            except:
                print("Ошибка преобразования выражения")
                cResp = ClientEquationResponse(error="Ошибка преобразования выражения")
            try:
                if x == x.evalf():
                    cResp = ClientEquationResponse(answer=f"Точно: {x}\nПримерно: {x.evalf()}")
                else:
                    cResp = ClientEquationResponse(answer=answer)
            except:
                cResp = ClientEquationResponse(error="Ошибка сборки ответа")

        return cResp
    
if __name__ == "__main__":
    print(WolframClient.request(""))'''

from handlers.del_wolfram_handler import WolframHandler
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from clients.wolfram.dto.wolfram_request_dto import WolframRequestDto
from clients.wolfram.dto.wolfram_response_dto import WolframResponseDto
from config.config import config
from settings import settings
from sympy import I, sympify, SympifyError
import requests

class WolframClient:
    def ask_question(self, data: ClientEquationRequest) -> ClientEquationResponse:
        cResp = ClientEquationResponse(error="Неизвестная ошибка")  # Инициализация по умолчанию
        try:
            req = WolframRequestDto(
                input=data.question,
                format="plaintext",
                output="JSON",
                appid=config.client_wolfram.appid
            )

            dReq = req.dict()

            print("REQUEST")
            print(dReq)

            response = requests.post(config.client_wolfram.url, data=dReq)

            print()
            print("Ответ пришел")
            print()

            if response.status_code == 200:
                try:
                    response.raise_for_status()
                    jsonResp = response.json()
                    print("RESPONSE")
                    print(jsonResp)
                    respDto = WolframResponseDto.parse_obj(jsonResp)
                except ValueError as e:
                    print(f"Ошибка разбора JSON: {e}")
                    return ClientEquationResponse(error=f"Ошибка разбора JSON: {e}")
                except Exception as e:
                    print(e)
                    return ClientEquationResponse(error=f"Ошибка преобразования ответа: {e}")
            else:
                print(f"Ошибка запроса: {response.status_code}")
                return ClientEquationResponse(error=f"Ошибка запроса: {response.status_code}")
            
            print()
            print("Ответ преобразовался")
            print()

            vs = ["", ""]
            sol_cnt = 0

            if respDto is not None:
                qResult = respDto.queryresult
                if qResult is not None and "pods" in qResult:
                    pods = qResult["pods"]
                    for pod in pods:
                        if "title" in pod and "numsubpods" in pod and ("Solution" in pod["title"] or "solution" in pod["title"]) and pod["numsubpods"] == 2:
                            if "subpods" in pod:
                                sol_cnt = 2
                                subpods = pod["subpods"]
                                vs = []
                                for subpod in subpods:
                                    if "plaintext" in subpod:
                                        vs.append(subpod["plaintext"])
                                print(vs)
                        elif "title" in pod and "numsubpods" in pod and ("Solution" in pod["title"] or "solution" in pod["title"]) and pod["numsubpods"] == 1:
                            if "subpods" in pod:
                                sol_cnt = 1
                                subpods = pod["subpods"]
                                if subpods and "plaintext" in subpods[0]:
                                    vs[0] = subpods[0]["plaintext"]
                                print(vs)
            
                    print()
                    print("Ответ разобрался")
                    print(sol_cnt)
                    print()

                else:
                    print("Empty answer")
            else:
                print("Модель не отвечает")
                print()
                print("Ответ не разобрался")
                print()
                return ClientEquationResponse(error="Модель не отвечает")
                

            answer = vs[0]

            if "i" in vs[0] or "i" in vs[1]:
                return ClientEquationResponse(answer="Дискриминант отрицательный. Нет действительных корней.")

            try:
                answer = answer[4:]
            except:
                pass                

            if sol_cnt == 2:
                print()
                print("Ответа два")
                print()
                try:
                    x = sympify(answer)
                    y = sympify(vs[1])
                except SympifyError as e:
                    print(f"Ошибка преобразования выражения: {e}")
                    return ClientEquationResponse(error=f"Ошибка преобразования выражения: {e}")
                print()
                print("Преобразовал")
                print()

                try:
                    if x != x.evalf() and y == y.evalf():
                        if x == x.evalf():
                            cResp = ClientEquationResponse(answer=answer, sol_count=sol_cnt)
                            cResp.answer2 = f"Точно: {y}\nПримерно: {y.evalf()}"
                        if y == y.evalf():
                            cResp = ClientEquationResponse(answer=f"Точно: {x}\nПримерно: {x.evalf()}", sol_count=sol_cnt)
                            cResp.answer2 = vs[1]
                    else:
                        cResp = ClientEquationResponse(answer=f"x = {answer}", answer2=f"x = {vs[1]}", sol_count=sol_cnt)
                except Exception as e:
                    print(f"Ошибка при обработке ответа: {e}")
                    return ClientEquationResponse(error=f"Ошибка при обработке ответа: {e}")

            elif sol_cnt == 1:
                print()
                print("Ответ один")
                print()
                try:
                    x = sympify(answer)
                    print("Преобразованное выражение:", x)
                    print("Численное значение:", x.evalf())
                except SympifyError as e:
                    print(f"Ошибка преобразования выражения: {e}")
                    return ClientEquationResponse(error=f"Ошибка преобразования выражения: {e}")
                print()
                print("Преобразовал")
                print()

                try:
                    if x == x.evalf():
                        cResp = ClientEquationResponse(answer=f"Точно: {x}\nПримерно: {x.evalf()}")
                    else:
                        cResp = ClientEquationResponse(answer=f"x = {answer}")
                except Exception as e:
                    print(f"Ошибка при обработке ответа: {e}")
                    return ClientEquationResponse(error=f"Ошибка при обработке ответа: {e}")

            return cResp

        except requests.exceptions.RequestException as e:
            print(e)
            return ClientEquationResponse(error=f"Ошибка запроса: {e}")
        except ValueError as e:
            print(e)
            return ClientEquationResponse(error=f"Не удалось преобразовать ответ: {e}")

if __name__ == "__main__":
    client = WolframClient()
    request_data = ClientEquationRequest(question="ваш_вопрос_здесь")
    print(client.ask_question(request_data))