.PHONY: dev prod down logs ps clean help rebuild run restart

# === Compose файл ===
COMPOSE_FILE := docker-compose.yaml

# === Окружение ===
ENV ?= dev

# ANSI colors
CYAN  := \033[36m
RESET := \033[0m

# === HELP ===
help: ## Показать доступные команды
	@echo "Использование: make [команда]"
	@echo ""
	@echo "Команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "Примеры:"
	@echo "  make up               - запуск dev"
	@echo "  make up ENV=prod      - запуск prod"
	@echo "  make logs service=api - логи сервиса"

# === UP ===
up: ## Запуск всех сервисов (dev/prod)
	@echo "🚀 Запуск ($(ENV))..."
	@docker compose -f $(COMPOSE_FILE) up -d
	@echo "✅ Готово!"

dev: ## Алиас для dev
	@$(MAKE) up ENV=dev

prod: ## Алиас для prod
	@$(MAKE) up ENV=prod

# === DOWN ===
down: ## Остановка всех сервисов
	@echo "⏹️ Остановка..."
	@docker compose -f $(COMPOSE_FILE) down
	@echo "✅ Остановлено!"

# === REBUILD ===
rebuild: ## Полная пересборка
	@echo "♻️ Пересборка ($(ENV))..."
	@docker compose -f $(COMPOSE_FILE) down || true
	@docker compose -f $(COMPOSE_FILE) build --no-cache
	@docker compose -f $(COMPOSE_FILE) up -d --force-recreate
	@echo "✅ Пересборка завершена!"

# === LOGS ===
logs: ## Логи (make logs service=api)
ifndef service
	@echo "❌ Укажи сервис: make logs service=api"
	@exit 1
else
	@docker compose -f $(COMPOSE_FILE) logs -f $(service)
endif

# === PS ===
ps: ## Статус контейнеров
	@docker compose -f $(COMPOSE_FILE) ps

# === CLEAN ===
clean: ## Полная очистка (контейнеры + volumes)
	@echo "🧹 Очистка..."
	@docker compose -f $(COMPOSE_FILE) down -v
	@echo "✅ Готово!"

# === RUN ONE SERVICE ===
run: ## Запуск одного сервиса (make run service=api)
ifndef service
	@echo "❌ Укажи сервис: make run service=api"
	@exit 1
else
	@echo "🚀 Запуск $(service)..."
	@docker compose -f $(COMPOSE_FILE) up -d --build $(service)
	@echo "✅ $(service) запущен!"
endif

# === RESTART ===
restart: ## Перезапуск сервиса (make restart service=api)
ifndef service
	@echo "❌ Укажи сервис"
	@exit 1
else
	@docker compose -f $(COMPOSE_FILE) restart $(service)
	@echo "🔁 $(service) перезапущен!"
endif

# === JOB ===
job-run: ## Одноразовый запуск job сервиса
ifndef service
	@echo "❌ Укажи сервис"
	@exit 1
else
	@docker compose -f $(COMPOSE_FILE) run --rm $(service)
endif