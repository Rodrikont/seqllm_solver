from environs import Env

class ConfigClientQwen:
        def __init__(self, env: Env):
#            self.host = env.str("CLIENT_QWEN_HOST", "")
            self.cycle_count = env.int("CLIENT_QWEN_CYLCE_COUNT", 6)

class Config:
    def __init__(self):
        env = Env()
        env.read_env()  # Загружает переменные из .env файла

        self.client_qwen = ConfigClientQwen(env)

        self.app_name = env.str("APP_NAME", "EqSolverLLM")
        self.app_version = env.str("APP_VERSION", "0.1")
        self.debug = env.bool("APP_DEBUG", False)
        self.host = env.str("APP_HOST", '0.0.0.0')
        self.port = env.int("APP_PORT", 8080)

config = Config()