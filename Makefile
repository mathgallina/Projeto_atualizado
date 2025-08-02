.PHONY: help install test lint clean run deploy backup rollback setup

# Variáveis
PYTHON = python3
PIP = pip
VENV = .venv
APP = app.py
PORT = 8001

# Cores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Mostrar esta ajuda
	@echo "$(BLUE)🚀 PROJET VELOZ - COMANDOS DISPONÍVEIS$(NC)"
	@echo "======================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Instalar dependências
	@echo "$(BLUE)📦 Instalando dependências...$(NC)"
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependências instaladas!$(NC)"

install-dev: ## Instalar dependências de desenvolvimento
	@echo "$(BLUE)📦 Instalando dependências de desenvolvimento...$(NC)"
	. $(VENV)/bin/activate && $(PIP) install -r requirements-dev.txt
	@echo "$(GREEN)✅ Dependências de desenvolvimento instaladas!$(NC)"

setup: ## Configurar projeto completo
	@echo "$(BLUE)🔧 Configurando projeto...$(NC)"
	./scripts/setup_project.sh -a
	@echo "$(GREEN)✅ Projeto configurado!$(NC)"

test: ## Executar testes
	@echo "$(BLUE)🧪 Executando testes...$(NC)"
	. $(VENV)/bin/activate && pytest tests/ -v
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

test-cov: ## Executar testes com cobertura
	@echo "$(BLUE)🧪 Executando testes com cobertura...$(NC)"
	. $(VENV)/bin/activate && pytest tests/ -v --cov=app --cov-report=html
	@echo "$(GREEN)✅ Testes com cobertura concluídos!$(NC)"

lint: ## Executar linting
	@echo "$(BLUE)🔍 Executando linting...$(NC)"
	. $(VENV)/bin/activate && flake8 app/ tests/
	@echo "$(GREEN)✅ Linting concluído!$(NC)"

format: ## Formatar código
	@echo "$(BLUE)🎨 Formatando código...$(NC)"
	. $(VENV)/bin/activate && black app/ tests/
	. $(VENV)/bin/activate && isort app/ tests/
	@echo "$(GREEN)✅ Código formatado!$(NC)"

clean: ## Limpar projeto
	@echo "$(BLUE)🧹 Limpando projeto...$(NC)"
	./scripts/cleanup.sh -a
	@echo "$(GREEN)✅ Projeto limpo!$(NC)"

run: ## Iniciar servidor
	@echo "$(BLUE)🚀 Iniciando servidor...$(NC)"
	./scripts/start_server.sh

run-dev: ## Iniciar servidor em modo desenvolvimento
	@echo "$(BLUE)🚀 Iniciando servidor em modo desenvolvimento...$(NC)"
	. $(VENV)/bin/activate && FLASK_ENV=development FLASK_DEBUG=True python $(APP)

deploy: ## Fazer deploy
	@echo "$(BLUE)🚀 Fazendo deploy...$(NC)"
	./scripts/deploy.sh -r $(REPO_URL) -e prod

backup: ## Criar backup
	@echo "$(BLUE)📦 Criando backup...$(NC)"
	./scripts/cleanup.sh -b

rollback: ## Fazer rollback
	@echo "$(BLUE)🔄 Fazendo rollback...$(NC)"
	./scripts/rollback.sh -l

git-init: ## Inicializar Git
	@echo "$(BLUE)🔧 Inicializando Git...$(NC)"
	./scripts/init_git.sh -c

git-tag: ## Criar tag
	@echo "$(BLUE)🏷️  Criando tag...$(NC)"
	git tag -a v$(VERSION) -m "Versão $(VERSION)"
	git push origin v$(VERSION)

security: ## Verificar segurança
	@echo "$(BLUE)🔒 Verificando segurança...$(NC)"
	. $(VENV)/bin/activate && safety check
	. $(VENV)/bin/activate && bandit -r app/

docs: ## Gerar documentação
	@echo "$(BLUE)📚 Gerando documentação...$(NC)"

compliance: ## Verificar conformidade com regras oficiais
	@echo "$(BLUE)🔍 Verificando conformidade...$(NC)"
	./scripts/compliance_check.sh
	. $(VENV)/bin/activate && sphinx-build -b html docs/ docs/_build/html

pre-commit: ## Instalar pre-commit hooks
	@echo "$(BLUE)🔧 Instalando pre-commit hooks...$(NC)"
	. $(VENV)/bin/activate && pre-commit install

pre-commit-run: ## Executar pre-commit hooks
	@echo "$(BLUE)🔧 Executando pre-commit hooks...$(NC)"
	. $(VENV)/bin/activate && pre-commit run --all-files

docker-build: ## Construir imagem Docker
	@echo "$(BLUE)🐳 Construindo imagem Docker...$(NC)"
	docker build -t projet-veloz .

docker-run: ## Executar container Docker
	@echo "$(BLUE)🐳 Executando container Docker...$(NC)"
	docker run -p $(PORT):$(PORT) projet-veloz

status: ## Mostrar status do projeto
	@echo "$(BLUE)📊 Status do projeto:$(NC)"
	@echo "🌿 Branch: $$(git branch --show-current)"
	@echo "📝 Último commit: $$(git log -1 --oneline)"
	@echo "🏷️  Tags: $$(git tag -l | tr '\n' ' ')"
	@echo "📦 Tamanho: $$(du -sh . | cut -f1)"
	@echo "🐍 Python: $$(python3 --version)"
	@echo "📁 Arquivos Python: $$(find . -name '*.py' | wc -l)"

# Comandos com parâmetros
deploy-with-repo: ## Fazer deploy com repositório (ex: make deploy-with-repo REPO_URL=https://github.com/user/repo.git)
	@echo "$(BLUE)🚀 Fazendo deploy...$(NC)"
	./scripts/deploy.sh -r $(REPO_URL) -e prod

rollback-to-commit: ## Fazer rollback para commit específico (ex: make rollback-to-commit COMMIT=abc123)
	@echo "$(BLUE)🔄 Fazendo rollback...$(NC)"
	./scripts/rollback.sh -c $(COMMIT)

rollback-to-tag: ## Fazer rollback para tag específica (ex: make rollback-to-tag TAG=v1.0.0)
	@echo "$(BLUE)🔄 Fazendo rollback...$(NC)"
	./scripts/rollback.sh -t $(TAG) 