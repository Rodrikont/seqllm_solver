from environs import Env
import os

class ConfigClientQwen:
     def __init__(self, env: Env):
        # self.host = env.str("CLIENT_QWEN_HOST", "")
        self.cycle_count = env.int("CLIENT_QWEN_CYLCE_COUNT", 6)
        self.q1 = env.str("REQUEST_1_TO_QWEN", "\nЭто уравнение? Уравнение может быть рациональным. Оно может содержать: простые значения, дробные значения, выражения. Внимательно проверь. Допустимый ответ только: Да или Нет. Комментарии не пиши.")
        self.q2 = env.str("REQUEST_2_TO_QWEN", "\nОно содержит только одну неизвестную? Допустимый ответ только: Да или Нет.")
        self.q3 = env.str("REQUEST_3_TO_QWEN", "\nВ нем есть ошибки? Допустимый ответ только: Да или Нет.")
        self.q4 = env.str("REQUEST_4_TO_QWEN", "\nОно линейное? Допустимый ответ только: Да или Нет")
        self.q5 = env.str("REQUEST_5_TO_QWEN", "\nОно квадратное? Допустимый ответ только: Да или Нет")
        self.q6 = env.str("REQUEST_6_TO_QWEN", "\nОно рациональное? Допустимый ответ только: Да или Нет")
        self.qs = [self.q1, self.q2, self.q3, self.q4, self.q5, self.q6]

class ConfigClientWolfram:
    def __init__(self, env: Env):
        self.url = env.str("CLIENT_WOLFRAM_URL", "http://api.wolframalpha.com/v2/query")
        self.appid = env.str("CLIENT_WOLFRAM_APPID", "")
        self.appid_file = env.str("CLIENT_WOLFRAM_APPID_FILE", "/run/secrets/seqllm_wolfram_appid")
        self.token = ""
    def init_token(self):
        if self.appid == "":
            # Проверка на существование файла
            if os.path.exists(self.appid_file):
                # Открытие файла и чтение содержимого
                with open(self.appid_file, "r", encoding="utf-8") as file:
                    self.token = file.read()
                self.appid = self.token
                print("Token created")
            else:
                print(f"Файл {self.appid_file} не существует.")

class Config:
    def __init__(self):
        env = Env()
        env.read_env()  # Загружает переменные из .env файла

        self.client_qwen = ConfigClientQwen(env)
        self.client_wolfram = ConfigClientWolfram(env)

        self.app_name = env.str("APP_NAME", "EqSolverLLM")
        self.app_version = env.str("APP_VERSION", "0.1.2")
        self.debug = env.bool("APP_DEBUG", False)
        self.host = env.str("APP_HOST", '0.0.0.0')
        self.port = env.int("APP_PORT", 8080)

config = Config()