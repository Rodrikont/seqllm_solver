from fastapi import FastAPI, Depends
from routes.equation_routes import router_e
from config.config import config
import uvicorn


config.client_wolfram.init_token()

# debug
'''print(vars(config))
print()
print(vars(config.client_qwen))
print()
print(vars(config.client_wolfram))
'''
app = FastAPI()

# Подключаем маршруты
app.include_router(router_e)

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
