# Используем базовый образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

#EXPOSE 8080

# Указываем команду для запуска приложения
CMD ["python", "main.py"]

# Указываем бесконечный запуск через sleep infinity
#ENTRYPOINT ["sleep", "infinity"]
