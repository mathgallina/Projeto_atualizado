#!/bin/bash

echo "🚀 CONFIGURAÇÃO COMPLETA - PROJET VELOZ"
echo "========================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Opções:"
    echo "  -h, --help          Mostra esta ajuda"
    echo "  -a, --all           Configuração completa"
    echo "  -g, --git           Configurar apenas Git"
    echo "  -c, --clean         Limpar projeto"
    echo "  -s, --start         Iniciar servidor"
    echo "  -t, --test          Executar testes"
    echo "  -b, --backup        Criar backup"
    echo ""
    echo "Exemplos:"
    echo "  $0 -a               # Configuração completa"
    echo "  $0 -g -c            # Git + limpeza"
    echo "  $0 -s               # Iniciar servidor"
}

# Função para mostrar progresso
show_progress() {
    local step="$1"
    local total="$2"
    local message="$3"
    
    echo -e "${BLUE}[$step/$total]${NC} $message"
}

# Função para verificar dependências
check_dependencies() {
    show_progress 1 8 "Verificando dependências do sistema..."
    
    local missing_deps=()
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi
    
    # Verificar pip
    if ! command -v pip &> /dev/null; then
        missing_deps+=("pip")
    fi
    
    # Verificar git
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${RED}❌ Dependências faltando:${NC}"
        for dep in "${missing_deps[@]}"; do
            echo "   • $dep"
        done
        echo ""
        echo "💡 Instale as dependências e tente novamente."
        exit 1
    fi
    
    echo -e "${GREEN}✅ Dependências verificadas!${NC}"
}

# Função para limpar projeto
clean_project() {
    show_progress 2 8 "Limpando projeto..."
    
    # Executar script de limpeza
    if [ -f "scripts/cleanup.sh" ]; then
        ./scripts/cleanup.sh -a
    else
        echo -e "${YELLOW}⚠️  Script de limpeza não encontrado.${NC}"
    fi
}

# Função para configurar Git
setup_git() {
    show_progress 3 8 "Configurando controle de versão..."
    
    if [ -f "scripts/init_git.sh" ]; then
        ./scripts/init_git.sh -c
    else
        echo -e "${YELLOW}⚠️  Script de Git não encontrado.${NC}"
    fi
}

# Função para configurar ambiente virtual
setup_venv() {
    show_progress 4 8 "Configurando ambiente virtual..."
    
    if [ ! -d ".venv" ]; then
        echo "📦 Criando ambiente virtual..."
        python3 -m venv .venv
    fi
    
    # Ativar ambiente virtual
    source .venv/bin/activate
    
    # Instalar dependências
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
    
    echo -e "${GREEN}✅ Ambiente virtual configurado!${NC}"
}

# Função para criar arquivo .env
create_env_file() {
    show_progress 5 8 "Configurando variáveis de ambiente..."
    
    if [ ! -f ".env" ]; then
        if [ -f "env.example" ]; then
            cp env.example .env
            echo -e "${GREEN}✅ Arquivo .env criado!${NC}"
            echo -e "${YELLOW}⚠️  Edite o arquivo .env com suas configurações.${NC}"
        else
            echo -e "${YELLOW}⚠️  Arquivo env.example não encontrado.${NC}"
        fi
    else
        echo -e "${GREEN}✅ Arquivo .env já existe.${NC}"
    fi
}

# Função para criar pastas necessárias
create_directories() {
    show_progress 6 8 "Criando estrutura de pastas..."
    
    local dirs=("logs" "backups" "docs" "tests")
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo "📁 Criada pasta: $dir"
        fi
    done
    
    # Criar arquivo .gitkeep em pastas vazias
    touch logs/.gitkeep
    touch backups/.gitkeep
    touch tests/.gitkeep
    
    echo -e "${GREEN}✅ Estrutura de pastas criada!${NC}"
}

# Função para testar aplicação
test_application() {
    show_progress 7 8 "Testando aplicação..."
    
    # Verificar se o servidor inicia
    echo "🧪 Testando inicialização do servidor..."
    
    # Parar servidor se estiver rodando
    if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null ; then
        lsof -ti:8001 | xargs kill -9
    fi
    
    # Testar se o app.py funciona
    if python3 -c "import app; print('✅ App importado com sucesso!')" 2>/dev/null; then
        echo -e "${GREEN}✅ Aplicação testada com sucesso!${NC}"
    else
        echo -e "${RED}❌ Erro ao testar aplicação!${NC}"
        return 1
    fi
}

# Função para mostrar resumo
show_summary() {
    show_progress 8 8 "Finalizando configuração..."
    
    echo ""
    echo -e "${GREEN}🎉 CONFIGURAÇÃO CONCLUÍDA!${NC}"
    echo "================================"
    echo ""
    echo "📋 Resumo da configuração:"
    echo "   ✅ Dependências verificadas"
    echo "   ✅ Projeto limpo"
    echo "   ✅ Git configurado"
    echo "   ✅ Ambiente virtual criado"
    echo "   ✅ Variáveis de ambiente configuradas"
    echo "   ✅ Estrutura de pastas criada"
    echo "   ✅ Aplicação testada"
    echo ""
    echo "🚀 Para iniciar o servidor:"
    echo "   ./scripts/start_server.sh"
    echo ""
    echo "📚 Scripts disponíveis:"
    echo "   • scripts/start_server.sh  - Iniciar servidor"
    echo "   • scripts/rollback.sh      - Fazer rollback"
    echo "   • scripts/deploy.sh        - Deploy em produção"
    echo "   • scripts/cleanup.sh       - Limpar projeto"
    echo ""
    echo "🌐 Acesse: http://localhost:8001"
    echo "👤 Login: admin"
    echo "🔑 Senha: admin123"
}

# Função para iniciar servidor
start_server() {
    echo "🚀 Iniciando servidor..."
    
    if [ -f "scripts/start_server.sh" ]; then
        ./scripts/start_server.sh
    else
        echo -e "${RED}❌ Script de inicialização não encontrado!${NC}"
        exit 1
    fi
}

# Função para executar testes
run_tests() {
    echo "🧪 Executando testes..."
    
    if [ -d "tests" ]; then
        python3 -m pytest tests/ -v
    else
        echo -e "${YELLOW}⚠️  Pasta de testes não encontrada.${NC}"
    fi
}

# Função para criar backup
create_backup() {
    echo "📦 Criando backup..."
    
    local backup_dir="backups/manual_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Copiar arquivos importantes
    cp -r app/ "$backup_dir/"
    cp -r templates/ "$backup_dir/"
    cp -r static/ "$backup_dir/"
    cp app.py "$backup_dir/"
    cp requirements.txt "$backup_dir/"
    
    echo -e "${GREEN}✅ Backup criado em: $backup_dir${NC}"
}

# Variáveis
SETUP_ALL="false"
SETUP_GIT="false"
CLEAN_PROJECT="false"
START_SERVER="false"
RUN_TESTS="false"
CREATE_BACKUP="false"

# Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -a|--all)
            SETUP_ALL="true"
            shift
            ;;
        -g|--git)
            SETUP_GIT="true"
            shift
            ;;
        -c|--clean)
            CLEAN_PROJECT="true"
            shift
            ;;
        -s|--start)
            START_SERVER="true"
            shift
            ;;
        -t|--test)
            RUN_TESTS="true"
            shift
            ;;
        -b|--backup)
            CREATE_BACKUP="true"
            shift
            ;;
        *)
            echo "❌ Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Se nenhuma opção foi especificada, fazer configuração completa
if [ "$SETUP_ALL" = "false" ] && [ "$SETUP_GIT" = "false" ] && [ "$CLEAN_PROJECT" = "false" ] && [ "$START_SERVER" = "false" ] && [ "$RUN_TESTS" = "false" ] && [ "$CREATE_BACKUP" = "false" ]; then
    SETUP_ALL="true"
fi

# Executar configuração completa
if [ "$SETUP_ALL" = "true" ]; then
    check_dependencies
    clean_project
    setup_git
    setup_venv
    create_env_file
    create_directories
    test_application
    show_summary
else
    # Executar ações específicas
    if [ "$CLEAN_PROJECT" = "true" ]; then
        clean_project
    fi
    
    if [ "$SETUP_GIT" = "true" ]; then
        setup_git
    fi
    
    if [ "$RUN_TESTS" = "true" ]; then
        run_tests
    fi
    
    if [ "$CREATE_BACKUP" = "true" ]; then
        create_backup
    fi
    
    if [ "$START_SERVER" = "true" ]; then
        start_server
    fi
fi

echo ""
echo -e "${GREEN}✨ Configuração finalizada!${NC}" 