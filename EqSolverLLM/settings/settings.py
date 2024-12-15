import json

WOLFRAM_URL = "http://api.wolframalpha.com/v2/query"
CLIENT_W_PORT = 1351
REQUEST_1_TO_QWEN = "\nЭто уравнение? Уравнение может быть рациональным. Оно может содержать: простые значения, дробные значения, выражения. Внимательно проверь. Допустимый ответ только: Да или Нет. Комментарии не пиши."
REQUEST_2_TO_QWEN = "\nОно содержит только одну неизвестную? Допустимый ответ только: Да или Нет."
REQUEST_3_TO_QWEN = "\nВ нем есть ошибки? Допустимый ответ только: Да или Нет."
REQUEST_4_TO_QWEN = "\nОно линейное? Допустимый ответ только: Да или Нет"
REQUEST_5_TO_QWEN = "\nОно квадратное? Допустимый ответ только: Да или Нет"
REQUEST_6_TO_QWEN = "\nОно рациональное? Допустимый ответ только: Да или Нет"
# REQUEST_7_TO_QWEN = "\nПокажи уравнение одной строкой. Не решай его."
# REQUEST_8_TO_QWEN = "\nРеши его и проверь ответы. Покажи только конечный ответ. Каждый корень в отдельной строке. Текстовые пояснения не показывай. Каждый ответ в новой строке. Дай ответ в простых дробях и десятичных дробях (точность до 5 знаков)."
# REQUEST_9_TO_QWEN = "\nУравнение преобразуй в формат API Wolfram метод GET для вставки в Postman.\nПокажи мне только значение input=..."
WELL_RESPONSE = json.dumps({
    "status": 200
})
WRONG_REQUEST_RESPONSE = json.dumps({
    "message": "Not Found",
    "status": 404
})
REQUESTS_TO_QWEN = [REQUEST_1_TO_QWEN, 
                    REQUEST_2_TO_QWEN, 
                    REQUEST_3_TO_QWEN, 
                    REQUEST_4_TO_QWEN, 
                    REQUEST_5_TO_QWEN, 
                    REQUEST_6_TO_QWEN, 
#                    REQUEST_7_TO_QWEN,
#                    REQUEST_8_TO_QWEN, 
#                    REQUEST_9_TO_QWEN
                        ]