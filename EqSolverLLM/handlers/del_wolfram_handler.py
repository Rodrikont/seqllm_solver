from handlers.handler_interface import HandlerInterface
from settings import settings
import sympy as sp
import requests

class WolframHandler(HandlerInterface):
    def request():
        pass
    
    def process_expression(expr_str):
        """
        Принимает строку с математическим выражением, содержащим floor и piecewise,
        преобразует её в sympy-выражение и упрощает его.
        """
        try:
            # Определяем переменные (можно расширить список при необходимости)
            B, x = sp.symbols('B x')
            
            # Функции для замены синтаксических элементов на SymPy-эквиваленты
            replacements = {
                'floor': 'sp.floor',
                'piecewise': 'sp.Piecewise',
                '^': '**',  # Заменяем возведение в степень для Python
                'mod': '%'
            }

            # Заменяем элементы выражения на совместимые с SymPy
            for old, new in replacements.items():
                expr_str = expr_str.replace(old, new)

            # Преобразуем строку в sympy-выражение
            expr = eval(expr_str, {"sp": sp, "B": B, "x": x})

            # Упрощаем выражение
            simplified_expr = sp.simplify(expr)

            return simplified_expr

        except Exception as e:
            return f"Ошибка обработки выражения: {e}"

    def execute(data):
        answ = WolframHandler.process_expression(WolframHandler.request(data))
        print(answ)
        return {"status": "success", "data": answ}
    