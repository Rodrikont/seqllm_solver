import json

WOLFRAM_URL = "http://api.wolframalpha.com/v2/query"
CLIENT_W_PORT = 1351
WELL_RESPONSE = json.dumps({
    "status": 200
})
WRONG_REQUEST_RESPONSE = json.dumps({
    "message": "Not Found",
    "status": 404
})

REQUESTS_REQUIRED_TO_QWEN = [
    "\nЭто уравнение? Уравнение может быть рациональным. Оно может содержать: простые значения, дробные значения, выражения. Внимательно проверь. Допустимый ответ только: Да или Нет. Комментарии не пиши.",
    "\nУравнение содержит только одну неизвестную? Допустимый ответ только: Да или Нет.",
]                    

REQUESTS_CONSISTENT_TO_QWEN = [
    "\nУравнение линейное? Допустимый ответ только: Да или Нет",
    "\nУравнение квадратное? Допустимый ответ только: Да или Нет",
    "\nОно рациональное? Допустимый ответ только: Да или Нет",
    "\nУравнение можно упростить до линейного? Допустимый ответ только: Да или Нет",
    "\nУравнение можно упростить до квадратного? Допустимый ответ только: Да или Нет",
]
