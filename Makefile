.PHONY: dev prod down logs ps clean help

# === Настройки ===
SERVICES := infra

SERVICE_DIR := services

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

down: ## Остановка всех сервисов
	@echo "⏹️  Остановка сервисов..."
	@for s in $(SERVICES); do \
		echo "⏸️  Остановка $$s..."; \
		docker compose -f $(SERVICE_DIR)/$$s/docker/base.yaml down || true; \
	done
	@echo "✅ Все остановлено!"

logs: ## Просмотр логов (использование: make logs service=browser_agent)
ifndef service
	@echo "❌ Ошибка: Укажите сервис. Пример: make logs service=browser_agent"
	@exit 1
else
	@echo "📜 Логи сервиса $(service)..."
	@docker compose -f $(SERVICE_DIR)/$(service)/docker/base.yaml logs -f
endif

ps: ## Показать статус всех сервисов
	@for s in $(SERVICES); do \
		echo ""; \
		echo "=== Сервис: $$s ==="; \
		docker compose -f $(SERVICE_DIR)/$$s/docker/base.yaml ps || true; \
	done

clean: ## Удалить все (контейнеры, volume-диски)
	@echo "🧹 Очистка сервисов..."
	@for s in $(SERVICES); do \
		echo "🧹 Очистка $$s..."; \
		docker compose -f $(SERVICE_DIR)/$$s/docker/base.yaml down -v || true; \
	done
	@echo "✅ Очистка завершена!"