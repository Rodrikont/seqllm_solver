from handlers.del_wolfram_handler import WolframHandler
from models.equation_data_response import EquationDataResponse
from settings import settings
import requests

class WolframClient():
    def request(data):
        try:
            params = {
                        'input': WolframHandler.convert(data),
                        'format': 'plaintext',
                        'output': 'JSON',
                        'appid': 'VTPUR2-T2TER673J7'
                        }
            response = requests.post(settings.WOLFRAM_URL, data=params)
            response.raise_for_status()  # Проверка статуса запроса
            response_data = response.json()
#            print(response_data) # uravnenie nado bylo
            if response_data is not None:
                        if 'queryresult' in response_data:
                            pods = response_data.get("queryresult").get("pods")
                            if pods and len(pods) >= 4:
                                subpods = pods[-1].get('subpods')
                                var = subpods[0].get('plaintext')
                                print(var) 
            answer: EquationDataResponse = var
        except requests.exceptions.RequestException as e:
            answer: EquationDataResponse = f"Request failed: {e}"
        except ValueError:
            answer: EquationDataResponse = "Failed to parse JSON response."
        return answer
    
if __name__ == '__main__':
    print(WolframClient.request(''))