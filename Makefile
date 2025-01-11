# Makefile
# fastHTTP server "npulse-watcher"

include .env
export

.DEFAULT_GOAL := help

################## help ##################
help: ## List of commands
	@awk 'BEGIN { \
		FS = ":.*##"; \
		printf "Usage: make <commands> \033[36m\033[0m\n" \
	} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { \
		printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 \
	} \
	/^##@/ { \
		printf "\n\033[1m%s\033[0m\n", substr($$0, 5) \
	} ' $(MAKEFILE_LIST)

server: ## Запуск fastHTTP сервера
	@echo "***** SERVER RUN *****"
	@set -o allexport; \
	. ./.app.env; \
	phyton main.py

img-build: ## Генерация образа docker контейнера
	docker build -t $(APP_IMG_NAME) .

img-rebuild: ## Удаление и генерация образа docker контейнера
	docker rmi $(APP_IMG_NAME)
	docker build -t $(APP_IMG_NAME) .

img-build-push: img-build img-push-local ## Сборка images, обновление в репозитарии и очистка
#	docker rmi $$(docker images --filter "reference=${APP_IMG}" -q)
	docker rmi $(APP_IMG_NAME)

img-push-local: ## Отправка images в локальный репозитарий
	docker tag $(APP_IMG_NAME) $(APP_IMG)
	docker push $(APP_IMG)
	docker rmi $(APP_IMG)

img-pull-local: ## Загрузка images из локального репозитария
	@docker pull $(APP_IMG)

docker-run: ## Запуск докера
	docker run -d --name $(APP_NAME) $(APP_IMG_NAME)

#secrets-create: ## Создание secrets
#	docker secret create npulse_telegram_token ./secrets/npulse_telegram_token

#secrets-rm: ## Создание secrets
#	docker secret rm npulse_telegram_token

stack-deploy: ## Развертывание контейнеров
	@docker stack deploy -c docker-compose.yml --detach=true $(STACK_NAME)

stack-rm: ## Удаление контейнеров
	@docker stack rm $(STACK_NAME)

install: stack-deploy ## Развертывание контейнеров

uninstall: stack-rm ## Удаление контейнеров
