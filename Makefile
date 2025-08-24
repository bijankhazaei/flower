.PHONY: help build up down logs shell test clean

help: ## Show this help message
	@echo "Flower Docker Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start development environment
	./scripts/docker-setup.sh

down: ## Stop all services
	docker-compose down

logs: ## View application logs
	docker-compose logs -f flower

shell: ## Access application shell
	docker-compose exec flower bash

test: ## Run tests
	docker-compose exec flower pytest

clean: ## Clean up Docker resources
	docker-compose down -v
	docker system prune -f

prod: ## Start production environment
	docker-compose up -d

dev: ## Start development environment with hot reload
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d