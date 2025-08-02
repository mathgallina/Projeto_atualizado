#!/bin/bash

echo "🚀 SISTEMA DE DEPLOY - PROJET VELOZ"
echo "===================================="
echo ""

# Configurações
PROJECT_NAME="projet_veloz"
PORT=8001
GIT_REPO=""
BACKUP_DIR="backups/deploy_$(date +%Y%m%d_%H%M%S)"

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Opções:"
    echo "  -h, --help          Mostra esta ajuda"
    echo "  -r, --repo URL      URL do repositório Git"
    echo "  -b, --branch BRANCH Branch para deploy (padrão: main)"
    echo "  -p, --port PORT     Porta do servidor (padrão: 8001)"
    echo "  -e, --env ENV       Ambiente (dev/prod, padrão: prod)"
    echo "  -k, --keep-backup   Manter backup após deploy"
    echo ""
    echo "Exemplos:"
    echo "  $0 -r https://github.com/user/projet_veloz.git"
    echo "  $0 -r https://github.com/user/projet_veloz.git -b dev"
    echo "  $0 -r https://github.com/user/projet_veloz.git -e dev"
}

# Função para criar backup
create_backup() {
    echo "📦 Criando backup do estado atual..."
    mkdir -p "$BACKUP_DIR"
    
    # Copiar arquivos importantes
    if [ -d "app" ]; then
        cp -r app/ "$BACKUP_DIR/"
    fi
    if [ -d "templates" ]; then
        cp -r templates/ "$BACKUP_DIR/"
    fi
    if [ -d "static" ]; then
        cp -r static/ "$BACKUP_DIR/"
    fi
    if [ -f "app.py" ]; then
        cp app.py "$BACKUP_DIR/"
    fi
    if [ -f "requirements.txt" ]; then
        cp requirements.txt "$BACKUP_DIR/"
    fi
    
    echo "✅ Backup criado em: $BACKUP_DIR"
}

# Função para verificar dependências
check_dependencies() {
    echo "🔍 Verificando dependências do sistema..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 não encontrado!"
        exit 1
    fi
    
    # Verificar pip
    if ! command -v pip &> /dev/null; then
        echo "❌ pip não encontrado!"
        exit 1
    fi
    
    # Verificar git
    if ! command -v git &> /dev/null; then
        echo "❌ Git não encontrado!"
        exit 1
    fi
    
    echo "✅ Dependências verificadas!"
}

# Função para parar servidor
stop_server() {
    echo "🛑 Parando servidor..."
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
        lsof -ti:$PORT | xargs kill -9
        echo "✅ Servidor parado!"
    else
        echo "ℹ️  Servidor não estava rodando."
    fi
}

# Função para clonar/atualizar repositório
update_repository() {
    local repo_url="$1"
    local branch="$2"
    
    echo "📥 Atualizando repositório..."
    
    if [ ! -d ".git" ]; then
        echo "🔄 Clonando repositório..."
        git clone -b "$branch" "$repo_url" temp_repo
        cp -r temp_repo/* .
        cp -r temp_repo/.* . 2>/dev/null || true
        rm -rf temp_repo
    else
        echo "🔄 Atualizando repositório existente..."
        git fetch origin
        git reset --hard "origin/$branch"
    fi
    
    echo "✅ Repositório atualizado!"
}

# Função para configurar ambiente
setup_environment() {
    local env="$1"
    
    echo "⚙️  Configurando ambiente: $env"
    
    # Criar ambiente virtual se não existir
    if [ ! -d ".venv" ]; then
        echo "📦 Criando ambiente virtual..."
        python3 -m venv .venv
    fi
    
    # Ativar ambiente virtual
    source .venv/bin/activate
    
    # Instalar dependências
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
    
    # Configurar variáveis de ambiente
    if [ "$env" = "prod" ]; then
        export FLASK_ENV=production
        export FLASK_DEBUG=False
    else
        export FLASK_ENV=development
        export FLASK_DEBUG=True
    fi
    
    echo "✅ Ambiente configurado!"
}

# Função para iniciar servidor
start_server() {
    local env="$1"
    
    echo "🚀 Iniciando servidor..."
    
    if [ "$env" = "prod" ]; then
        echo "🏭 Modo produção com Gunicorn..."
        gunicorn -w 4 -b 0.0.0.0:$PORT app:app --daemon
    else
        echo "🔧 Modo desenvolvimento..."
        python3 app.py &
    fi
    
    # Aguardar servidor iniciar
    sleep 3
    
    # Verificar se servidor está rodando
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Servidor iniciado com sucesso!"
        echo "🌐 Acesse: http://localhost:$PORT"
    else
        echo "❌ Erro ao iniciar servidor!"
        exit 1
    fi
}

# Função para limpar backup
cleanup_backup() {
    if [ "$KEEP_BACKUP" != "true" ]; then
        echo "🧹 Limpando backup..."
        rm -rf "$BACKUP_DIR"
        echo "✅ Backup removido!"
    else
        echo "💾 Backup mantido em: $BACKUP_DIR"
    fi
}

# Variáveis
GIT_REPO=""
BRANCH="main"
ENVIRONMENT="prod"
KEEP_BACKUP="false"

# Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -r|--repo)
            GIT_REPO="$2"
            shift 2
            ;;
        -b|--branch)
            BRANCH="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -k|--keep-backup)
            KEEP_BACKUP="true"
            shift
            ;;
        *)
            echo "❌ Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Verificar se repositório foi especificado
if [ -z "$GIT_REPO" ]; then
    echo "❌ Erro: URL do repositório é obrigatória!"
    echo ""
    show_help
    exit 1
fi

# Verificar se porta é válida
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "❌ Erro: Porta inválida: $PORT"
    exit 1
fi

echo "🚀 Iniciando deploy..."
echo "📋 Configurações:"
echo "   • Repositório: $GIT_REPO"
echo "   • Branch: $BRANCH"
echo "   • Porta: $PORT"
echo "   • Ambiente: $ENVIRONMENT"
echo ""

# Executar etapas do deploy
check_dependencies
create_backup
stop_server
update_repository "$GIT_REPO" "$BRANCH"
setup_environment "$ENVIRONMENT"
start_server "$ENVIRONMENT"
cleanup_backup

echo ""
echo "🎉 Deploy concluído com sucesso!"
echo "📊 Status do servidor:"
lsof -i :$PORT 