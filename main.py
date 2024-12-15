from fastapi import FastAPI, Depends
from routes.equation_routes import router_e
from config.config import config
from usecases.equation_usecase import EquationUseCase

# debug
print(vars(config))
print(vars(config.client_qwen))

app = FastAPI()

# Подключаем маршруты
app.include_router(router_e)

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)