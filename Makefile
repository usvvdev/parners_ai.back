.PHONY: dev prod down logs ps clean help

# === Настройки ===
SERVICE_DIR := services

# 1. Автоматически находим все папки внутри $(SERVICE_DIR)/
# Звездочка со слешем на конце (/*/) гарантирует, что мы ищем ТОЛЬКО директории
_SERVICE_PATHS := $(wildcard $(SERVICE_DIR)/*/)

# 2. Очищаем пути и сортируем: infra должна быть первой
RAW_SERVICES := $(notdir $(patsubst %/,%,$(_SERVICE_PATHS)))

# Находим infra (если она есть) и все остальные сервисы
INFRA_SERVICE := $(filter infra, $(RAW_SERVICES))
OTHER_SERVICES := $(filter-out infra, $(RAW_SERVICES))

# Склеиваем список: infra всегда будет первой, затем все остальное
ALL_SERVICES := $(INFRA_SERVICE) $(OTHER_SERVICES)

# 3. Мягкое присваивание! 
# Если вы не передали SERVICES в консоли, Make будет использовать ВСЕ найденные сервисы.
SERVICES ?= $(ALL_SERVICES)

COMPOSE_DIR := docker
BASE_FILE := $(COMPOSE_DIR)/base.yaml
DEV_FILE := $(COMPOSE_DIR)/development.yaml
PROD_FILE := $(COMPOSE_DIR)/production.yaml

# ANSI-цвета для вывода в терминале
CYAN  := \033[36m
RESET := \033[0m

# === Команды ===

help: ## Показать доступные команды
	@echo "Использование: make [команда]"
	@echo ""
	@echo "Команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-10s$(RESET) %s\n", $$1, $$2}'

dev: ## Запуск всех сервисов (dev)
	@echo "🚀 Запуск сервисов (dev)..."
	@for s in $(SERVICES); do \
		echo "▶️  Запуск $$s..."; \
		docker compose \
			--project-directory $(SERVICE_DIR)/$$s \
			-f $(SERVICE_DIR)/$$s/docker/base.yaml \
			-f $(SERVICE_DIR)/$$s/docker/development.yaml \
			up -d || exit 1; \
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
	done
	@echo "✅ Продакшн окружение готово!"

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