# Makefile
# fastHTTP server "SeqLLM solver"

include .make.env
export

VERSION_APP_FILE := "VERSION"
VERSION_IMG_FILE := "VERSION_IMG"

VERSION_APP_START := "0.1.0"
VERSION_IMG_START := "0.1.0"

VERSION_IMG := $(shell cat $(VERSION_IMG_FILE))
VERSION_IMG_NEW := $(shell echo $(VERSION_IMG) | awk -F. '{print $$1"."$$2"."$$3+1}')

VERSION_APP := $(shell cat $(VERSION_APP_FILE))
VERSION_APP_NEW := $(shell echo $(VERSION_APP) | awk -F. '{print $$1"."$$2"."$$3+1}')

APP_IMG_VERSION := $(APP_IMG):$(VERSION_IMG)
APP_IMG_VERSION_NEW := $(APP_IMG):$(VERSION_IMG_NEW)

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

img-rebuild-push: img-rebuild img-push ## Сборка images, обновление в репозитарии и очистка
#	docker rmi $$(docker images --filter "reference=${APP_IMG}" -q)

img-rm: ## Удаление image с тегом latest
	-docker rmi -f $(APP_IMG_NAME)

img-push: ## Отправка images в локальный репозитарий с тегом latest
	docker tag $(APP_IMG_NAME) $(APP_IMG_LATEST)
	docker push $(APP_IMG_LATEST)
	docker rmi $(APP_IMG_LATEST)

img-push-version: ## Отправка images в локальный репозитарий с тегом актуальной версии
	docker tag $(APP_IMG_NAME) $(APP_IMG_VERSION)
	docker push $(APP_IMG_VERSION)
	docker rmi $(APP_IMG_VERSION)

img-pull: ## Загрузка images из локального репозитария
	@docker pull $(APP_IMG_LATEST)

docker-run: ## Запуск докера
	docker run -d --name $(APP_NAME) $(APP_IMG_NAME_LATEST)

git-push-tag-version: ## Создание тега в git для актуальной версии
	-git tag v$(VERSION_APP)
	git push --tags

venv-recreate: ## Переустанвка venv
	rm -rf .venv
	python3 -m venvenv

venv-pip-install: ## venv-pip-install
	pip install --upgrade pip
	pip install --no-cache-dir -r requirements.txt

version-img-create: ## Создание файла с номер версии images
	echo -n $(VERSION_IMG_START) > $(VERSION_IMG_FILE)

version-app-create: ## Создание файла с номер версии программы
	echo -n $(VERSION_APP_START) > $(VERSION_APP_FILE)

version-img-inc: ## Увеличение номера версии images и сохранение в файл
	echo -n $(VERSION_IMG_NEW) > $(VERSION_IMG_FILE)

version-app-inc: ## Увеличение номера версии программы и сохранение в файл
	echo -n $(VERSION_APP_NEW) > $(VERSION_APP_FILE)

version-img-list: ## Список версий images
	curl -s $(DOCKER_HTTP_ADRR_TAG_LIST) | jq .
