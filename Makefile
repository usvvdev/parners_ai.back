.PHONY: dev prod down logs ps clean help rebuild run restart

# === Настройки ===
SERVICE_DIR := services

# 1. Автоматически находим все папки внутри $(SERVICE_DIR)/
_SERVICE_PATHS := $(wildcard $(SERVICE_DIR)/*/)

# 2. Очищаем пути и сортируем: infra должна быть первой
RAW_SERVICES := $(notdir $(patsubst %/,%,$(_SERVICE_PATHS)))

INFRA_SERVICE := $(filter infra, $(RAW_SERVICES))
OTHER_SERVICES := $(filter-out infra, $(RAW_SERVICES))

ALL_SERVICES := $(INFRA_SERVICE) $(OTHER_SERVICES)

# 3. Мягкое присваивание списка сервисов
SERVICES ?= $(ALL_SERVICES)

# === Окружение для Rebuild ===
# По умолчанию используем dev. Для продакшена: make rebuild ENV=prod
ENV ?= dev
ifeq ($(ENV),prod)
	TARGET_FILE := production.yaml
else
	TARGET_FILE := development.yaml
endif

# ANSI-цвета для вывода в терминале
CYAN  := \033[36m
RESET := \033[0m

# === Команды ===

help: ## Показать доступные команды
	@echo "Использование: make [команда]"
	@echo ""
	@echo "Команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "Примеры:"
	@echo "  make rebuild              - Полная пересборка (dev) с паузой для infra"
	@echo "  make rebuild ENV=prod     - Полная пересборка (production) с паузой для infra"
	@echo "  make logs service=api     - Просмотр логов конкретного сервиса"

dev: ## Запуск всех сервисов (dev)
	@echo "🚀 Запуск сервисов (dev)..."
	@for s in $(SERVICES); do \
		echo "▶️  Запуск $$s..."; \
		docker compose \
			--project-directory $(SERVICE_DIR)/$$s \
			-f $(SERVICE_DIR)/$$s/docker/base.yaml \
			-f $(SERVICE_DIR)/$$s/docker/development.yaml \
			up -d || exit 1; \
		if [ "$$s" = "infra" ]; then \
			echo "⏳ Ожидание 15 секунд для инициализации баз данных..."; \
			sleep 15; \
		fi; \
	done
	@echo "✅ Все запущено!"

prod: ## Запуск всех сервисов (production)
	@echo "🚀 Запуск сервисов (production)..."
	@for s in $(SERVICES); do \
		echo "▶️  Запуск $$s..."; \
		docker compose \
			--project-directory $(SERVICE_DIR)/$$s \
			-f $(SERVICE_DIR)/$$s/docker/base.yaml \
			-f $(SERVICE_DIR)/$$s/docker/production.yaml \
			up -d || exit 1; \
		if [ "$$s" = "infra" ]; then \
			echo "⏳ Ожидание 15 секунд для инициализации баз данных..."; \
			sleep 15; \
		fi; \
	done
	@echo "✅ Продакшн окружение готово!"

rebuild: ## Полная пересборка (использование: make rebuild [ENV=prod])
	@echo "♻️  Пересборка сервисов (Окружение: $(ENV))..."
	@for s in $(SERVICES); do \
		echo "⏹️  Удаление старых контейнеров $$s..."; \
		docker compose \
			--project-directory $(SERVICE_DIR)/$$s \
			-f $(SERVICE_DIR)/$$s/docker/base.yaml \
			down || true; \
		echo "🔨 Сборка $$s без кэша..."; \
		docker compose \
			--project-directory $(SERVICE_DIR)/$$s \
			-f $(SERVICE_DIR)/$$s/docker/base.yaml \
			-f $(SERVICE_DIR)/$$s/docker/$(TARGET_FILE) \
			build --no-cache; \
		echo "▶️  Запуск $$s..."; \
		docker compose \
			--project-directory $(SERVICE_DIR)/$$s \
			-f $(SERVICE_DIR)/$$s/docker/base.yaml \
			-f $(SERVICE_DIR)/$$s/docker/$(TARGET_FILE) \
			up -d --force-recreate || exit 1; \
		if [ "$$s" = "infra" ]; then \
			echo "⏳ Ожидание 15 секунд для инициализации баз данных..."; \
			sleep 15; \
		fi; \
	done
	@echo "✅ Пересборка ($(ENV)) завершена!"

down: ## Остановка всех сервисов (в обратном порядке)
	@echo "⏹️  Остановка сервисов..."
	@for s in $(OTHER_SERVICES) $(INFRA_SERVICE); do \
		if echo "$(SERVICES)" | grep -wq "$$s"; then \
			echo "⏸️  Остановка $$s..."; \
			docker compose \
				--project-directory $(SERVICE_DIR)/$$s \
				-f $(SERVICE_DIR)/$$s/docker/base.yaml \
				down || true; \
		fi \
	done
	@echo "✅ Все остановлено!"

logs: ## Просмотр логов (использование: make logs service=browser_agent)
ifndef service
	@echo "❌ Ошибка: Укажите сервис. Пример: make logs service=browser_agent"
	@exit 1
else
	@echo "📜 Логи сервиса $(service)..."
	@docker compose \
		--project-directory $(SERVICE_DIR)/$(service) \
		-f $(SERVICE_DIR)/$(service)/docker/base.yaml \
		logs -f
endif

ps: ## Показать статус всех сервисов
	@for s in $(SERVICES); do \
		echo ""; \
		echo "=== Сервис: $$s ==="; \
		docker compose \
			--project-directory $(SERVICE_DIR)/$$s \
			-f $(SERVICE_DIR)/$$s/docker/base.yaml \
			ps || true; \
	done

clean: ## Удалить все (контейнеры, volume-диски) в обратном порядке
	@echo "🧹 Очистка сервисов..."
	@for s in $(OTHER_SERVICES) $(INFRA_SERVICE); do \
		if echo "$(SERVICES)" | grep -wq "$$s"; then \
			echo "🧹 Очистка $$s..."; \
			docker compose \
				--project-directory $(SERVICE_DIR)/$$s \
				-f $(SERVICE_DIR)/$$s/docker/base.yaml \
				down -v || true; \
		fi \
	done
	@echo "✅ Очистка завершена!"

run: ## Запуск одного сервиса (использование: make run service=api ENV=dev|prod)
ifndef service
	@echo "❌ Укажи сервис: make run service=api"
	@exit 1
else
	@echo "🚀 Запуск сервиса $(service) (ENV=$(ENV))..."
	@docker compose \
		--project-directory $(SERVICE_DIR)/$(service) \
		-f $(SERVICE_DIR)/$(service)/docker/base.yaml \
		-f $(SERVICE_DIR)/$(service)/docker/$(TARGET_FILE) \
		up -d --build
	@echo "✅ Сервис $(service) запущен!"
endif

restart: ## Перезапуск одного сервиса (make restart service=api)
ifndef service
	@echo "❌ Укажи сервис: make restart service=api"
	@exit 1
else
	@echo "🔁 Перезапуск $(service)..."
	@docker compose \
		--project-directory $(SERVICE_DIR)/$(service) \
		-f $(SERVICE_DIR)/$(service)/docker/base.yaml \
		down || true
	@docker compose \
		--project-directory $(SERVICE_DIR)/$(service) \
		-f $(SERVICE_DIR)/$(service)/docker/base.yaml \
		-f $(SERVICE_DIR)/$(service)/docker/$(TARGET_FILE) \
		up -d --build
	@echo "✅ $(service) перезапущен!"
endif

job-run: ## Запуск одноразового job сервиса
ifndef service
	@echo "❌ Укажи сервис: make job-run service=browser_agent"
	@exit 1
else
	@echo "⚡ Job запуск $(service)..."
	@docker compose \
		--project-directory $(SERVICE_DIR)/$(service) \
		-f $(SERVICE_DIR)/$(service)/docker/base.yaml \
		-f $(SERVICE_DIR)/$(service)/docker/$(TARGET_FILE) \
		run --rm $(service)
endif