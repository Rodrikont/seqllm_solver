# Makefile
# servervice "telegram bot"

include .make.env
export

APP_VERSION_START := "0.0.0"
APP_VERSION := $(shell cat VERSION)
APP_VERSION_NEW := $(shell echo $(APP_VERSION) | awk -F. '{print $$1"."$$2"."$$3+1}')
APP_IMG_VERSION := $(APP_IMG):$(APP_VERSION)
APP_IMG_VERSION_NEW := $(APP_IMG):$(APP_VERSION_NEW)

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
	. ./.env; \
	python3 main.py

server-myenv: ## Запуск fastHTTP сервера в myenv окружении
	python3 -m venv myenv
	source myenv/bin/activate
	@echo "***** SERVER RUN *****"
	@set -o allexport; \
	. ./.env; \
	python3 main.py

img-build: ## Генерация образа docker контейнера
	docker build -t $(APP_IMG_NAME) .

img-rebuild: ## Удаление и генерация образа docker контейнера
	docker rmi -f $(APP_IMG_NAME)
	docker build -t $(APP_IMG_NAME) .

img-build-push-rm: img-rebuild img-push-local ## Сборка images, обновление в репозитарии и очистка
#	docker rmi $$(docker images --filter "reference=${APP_IMG}" -q)
	docker rmi -f $(APP_IMG_NAME)

img-push-local: ## Отправка images в локальный репозитарий
	docker tag $(APP_IMG_NAME) $(APP_IMG_LATEST)
	docker push $(APP_IMG_LATEST)
	docker rmi $(APP_IMG_LATEST)
	docker tag $(APP_IMG_NAME) $(APP_IMG_VERSION_NEW)
	docker push $(APP_IMG_VERSION_NEW)
	docker rmi $(APP_IMG_VERSION_NEW)
	@$(MAKE) -s version-inc

img-pull-local: ## Загрузка images из локального репозитария
	@docker pull $(APP_IMG_LATEST)

docker-run: ## Запуск докера
	docker run -d --name $(APP_NAME) $(APP_IMG_NAME_LATEST)

venv-recreate: ## Переустанвка venv
	rm -rf .venv
	python3 -m venvenv

venv-pip-install: ## venv-pip-install
	pip install --upgrade pip
	pip install --no-cache-dir -r requirements.txt

version-create: ## Создание файла с номер версии
	echo $(APP_VERSION_START) > VERSION

version-inc: ## Увеличение номера версии и сохранение в файл
	echo $(APP_VERSION_NEW) > VERSION

version-list: ## Список версий
	curl -s $(DOCKER_HTTP_ADRR_TAG_LIST) | jq .
