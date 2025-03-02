from handlers.del_wolfram_handler import WolframHandler
from models.client_equation_request import ClientEquationRequest
from models.client_equation_response import ClientEquationResponse
from clients.wolfram.dto.wolfram_request_dto import WolframRequestDto
from clients.wolfram.dto.wolfram_response_dto import WolframResponseDto
from config.config import config
from enums.status_enums import Status
from sympy import I, sympify, SympifyError, Float, Integer
import requests, re

class WolframClient:
    def ask_question(self, data: ClientEquationRequest) -> ClientEquationResponse:
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
                    return ClientEquationResponse(status=Status.ERROR.value, error=f"Ошибка разбора JSON: {e}")
                except Exception as e:
                    print(e)
                    return ClientEquationResponse(status=Status.ERROR.value, error=f"Ошибка преобразования ответа: {e}")
            else:
                print(f"Ошибка запроса: {response.status_code}")
                return ClientEquationResponse(status=Status.ERROR.value, error=f"Ошибка запроса: {response.status_code}")
            
            print()
            print("Ответ преобразовался")
            print()

            roots = []
            aproxRoots = []

            if respDto is not None:
                qResult = respDto.queryresult
                if qResult is not None and "pods" in qResult:
                    pods = qResult["pods"]
                    for pod in pods:
                        if "title" in pod and "numsubpods" in pod and ("Solution" in pod["title"] or "solution" in pod["title"]):
                            if "subpods" in pod:
                                subpods = pod["subpods"]
                                for subpod in subpods:
                                    if "plaintext" in subpod:
                                        roots.append(subpod["plaintext"])
                                print(roots)

                    print()
                    print("Ответ разобрался")
                    print()

                else:
                    print("Empty answer")
            else:
                print("Модель не отвечает")
                print()
                print("Ответ не разобрался")
                print()
                return ClientEquationResponse(
                    status=Status.ERROR.value,
                    error="Модель не отвечает",
                )

            prefixRoots = []
            sufixRoots = []

            status = Status.CALCULATED.value

            for i in range(len(roots)):
                root = re.sub(r'(\d+)\s*([a-zA-Z\(])', r'\1*\2', roots[i])
                roots[i] = root
                prefixRoots.append(root[:4])
                sufixRoots.append(root[4:])
            
            try:
                for i in range(len(sufixRoots)):
                    # Выполняем упрощение и затем округление, если это возможно
                    root = sympify(sufixRoots[i])
                    fResult = root.evalf()
                    if isinstance(fResult, (Float, Integer)):
                        # Преобразование в текст и удаление лишних нулей в дробной части
                        sResult = f"{fResult:.10f}".rstrip('0').rstrip('.') if "." in f"{fResult:.10f}" else f"{fResult:.10f}"
                        aproxRoots.append(prefixRoots[i] + sResult)           
                # Если количество корней отличается, то очищаем корни с округлением
                if len(aproxRoots) != len(roots):
                    aproxRoots = []
                # Если после округления результат не изменился, то очищаем корни с округлением
                if len(aproxRoots) > 0:
                    isDiff = False
                    for i in range(len(roots)):
                        if roots[i] != aproxRoots[i]:
                            isDiff = True
                            break
                    if isDiff == False:
                        aproxRoots = []
            except SympifyError as e:
                print(f"Ошибка преобразования выражения: {e}")
                answer = f"Ошибка преобразования выражения: {e}",
            
            print()
            print("Преобразовал")
            print()

            if len(roots) == 0:
                return ClientEquationResponse(
                    status=Status.ERROR.value,
                    error="Нет корней",
                )

            error = None
            if len(roots) > 2:
                status = Status.CALCULATED_MORE_ROOTS.value
                error = "Найдено больше 2-х корней"

            answer = None
            for root in roots:
                if "i" in root:
                    status=Status.NEGATIVE_DISCRIMINANT.value
                    answer="Дискриминант отрицательный. Нет рациональных корней."
                    break

            return ClientEquationResponse(
                status=status,
                roots=roots,
                aproxRoots=aproxRoots,
                answer=answer,
                error=error,
            )

        except requests.exceptions.RequestException as e:
            print(e)
            return ClientEquationResponse(
                status=Status.ERROR.value,
                error=f"Ошибка запроса: {e}",
            )
        except ValueError as e:
            print(e)
            return ClientEquationResponse(
                status=Status.ERROR.value,
                error=f"Не удалось преобразовать ответ: {e}",
            )

if __name__ == "__main__":
    client = WolframClient()
    request_data = ClientEquationRequest(question="")
    print(client.ask_question(request_data))
