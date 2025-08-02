#!/bin/bash

echo "🔄 SISTEMA DE ROLLBACK - PROJET VELOZ"
echo "======================================"
echo ""

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Opções:"
    echo "  -h, --help          Mostra esta ajuda"
    echo "  -l, --list          Lista commits disponíveis"
    echo "  -c, --commit HASH   Faz rollback para commit específico"
    echo "  -t, --tag TAG       Faz rollback para tag específica"
    echo "  -1, --last          Faz rollback para o último commit"
    echo "  -b, --backup        Cria backup antes do rollback"
    echo ""
    echo "Exemplos:"
    echo "  $0 -l                    # Lista commits"
    echo "  $0 -c abc123            # Rollback para commit abc123"
    echo "  $0 -t v1.0.0           # Rollback para tag v1.0.0"
    echo "  $0 -1                   # Rollback para último commit"
    echo "  $0 -b -c abc123         # Backup + rollback"
}

# Função para criar backup
create_backup() {
    echo "📦 Criando backup do estado atual..."
    backup_dir="backups/rollback_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Fazer stash das mudanças não commitadas
    git stash push -m "Backup antes do rollback $(date)"
    
    # Copiar arquivos importantes
    cp -r app/ "$backup_dir/"
    cp -r templates/ "$backup_dir/"
    cp -r static/ "$backup_dir/"
    cp app.py "$backup_dir/"
    cp requirements.txt "$backup_dir/"
    
    echo "✅ Backup criado em: $backup_dir"
}

# Função para listar commits
list_commits() {
    echo "📋 Últimos commits disponíveis:"
    echo ""
    git log --oneline -10
    echo ""
    echo "📋 Tags disponíveis:"
    echo ""
    git tag -l | tail -10
}

# Função para fazer rollback
do_rollback() {
    local target="$1"
    local is_tag="$2"
    
    echo "🔄 Iniciando rollback..."
    
    # Parar servidor se estiver rodando
    if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null ; then
        echo "🛑 Parando servidor..."
        lsof -ti:8001 | xargs kill -9
    fi
    
    # Fazer rollback
    if [ "$is_tag" = "true" ]; then
        echo "🏷️  Fazendo rollback para tag: $target"
        git checkout "$target"
    else
        echo "📝 Fazendo rollback para commit: $target"
        git reset --hard "$target"
    fi
    
    # Reinstalar dependências se necessário
    echo "📦 Verificando dependências..."
    source .venv/bin/activate
    pip install -r requirements.txt
    
    echo "✅ Rollback concluído!"
    echo ""
    echo "🚀 Para iniciar o servidor:"
    echo "   ./scripts/start_server.sh"
}

# Variáveis
BACKUP=false
COMMIT_HASH=""
TAG_NAME=""
LIST_COMMITS=false
LAST_COMMIT=false

# Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -l|--list)
            LIST_COMMITS=true
            shift
            ;;
        -c|--commit)
            COMMIT_HASH="$2"
            shift 2
            ;;
        -t|--tag)
            TAG_NAME="$2"
            shift 2
            ;;
        -1|--last)
            LAST_COMMIT=true
            shift
            ;;
        -b|--backup)
            BACKUP=true
            shift
            ;;
        *)
            echo "❌ Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Verificar se estamos em um repositório Git
if [ ! -d ".git" ]; then
    echo "❌ Erro: Não é um repositório Git!"
    echo "💡 Execute 'git init' para inicializar o repositório."
    exit 1
fi

# Listar commits se solicitado
if [ "$LIST_COMMITS" = "true" ]; then
    list_commits
    exit 0
fi

# Verificar se pelo menos uma opção de rollback foi especificada
if [ -z "$COMMIT_HASH" ] && [ -z "$TAG_NAME" ] && [ "$LAST_COMMIT" = "false" ]; then
    echo "❌ Erro: Especifique uma opção de rollback!"
    echo ""
    show_help
    exit 1
fi

# Criar backup se solicitado
if [ "$BACKUP" = "true" ]; then
    create_backup
fi

# Executar rollback
if [ "$LAST_COMMIT" = "true" ]; then
    do_rollback "HEAD~1" "false"
elif [ -n "$TAG_NAME" ]; then
    do_rollback "$TAG_NAME" "true"
elif [ -n "$COMMIT_HASH" ]; then
    do_rollback "$COMMIT_HASH" "false"
fi 