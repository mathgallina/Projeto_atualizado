#!/bin/bash

echo "🧹 SISTEMA DE LIMPEZA - PROJET VELOZ"
echo "====================================="
echo ""

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Opções:"
    echo "  -h, --help          Mostra esta ajuda"
    echo "  -a, --all           Limpeza completa (inclui logs e cache)"
    echo "  -c, --cache         Limpar apenas cache Python"
    echo "  -l, --logs          Limpar apenas logs"
    echo "  -t, --temp          Limpar arquivos temporários"
    echo "  -b, --backup        Limpar backups antigos (mais de 30 dias)"
    echo "  -d, --dry-run       Mostrar o que seria removido (não executa)"
    echo ""
    echo "Exemplos:"
    echo "  $0 -a               # Limpeza completa"
    echo "  $0 -c               # Limpar cache Python"
    echo "  $0 -l -t            # Limpar logs e arquivos temporários"
    echo "  $0 -d -a            # Simular limpeza completa"
}

# Função para limpar cache Python
clean_python_cache() {
    echo "🐍 Limpando cache Python..."
    
    # Remover __pycache__
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    
    # Remover arquivos .pyc
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Remover arquivos .pyo
    find . -name "*.pyo" -delete 2>/dev/null || true
    
    # Remover .pytest_cache
    find . -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    
    # Remover .coverage
    find . -name ".coverage" -delete 2>/dev/null || true
    
    # Remover htmlcov
    find . -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
    
    echo "✅ Cache Python limpo!"
}

# Função para limpar logs
clean_logs() {
    echo "📝 Limpando logs..."
    
    if [ -d "logs" ]; then
        if [ "$DRY_RUN" = "true" ]; then
            echo "📋 Logs que seriam removidos:"
            find logs/ -type f -name "*.log" -ls
        else
            find logs/ -type f -name "*.log" -delete
            echo "✅ Logs limpos!"
        fi
    else
        echo "ℹ️  Pasta logs não encontrada."
    fi
}

# Função para limpar arquivos temporários
clean_temp_files() {
    echo "🗂️  Limpando arquivos temporários..."
    
    # Arquivos temporários comuns
    local temp_patterns=(
        "*.tmp"
        "*.temp"
        "*.swp"
        "*.swo"
        "*~"
        ".DS_Store"
        "Thumbs.db"
        "ehthumbs.db"
    )
    
    for pattern in "${temp_patterns[@]}"; do
        if [ "$DRY_RUN" = "true" ]; then
            find . -name "$pattern" -ls 2>/dev/null || true
        else
            find . -name "$pattern" -delete 2>/dev/null || true
        fi
    done
    
    # Limpar pastas temporárias
    local temp_dirs=("tmp" "temp" ".tmp" ".temp")
    for dir in "${temp_dirs[@]}"; do
        if [ -d "$dir" ]; then
            if [ "$DRY_RUN" = "true" ]; then
                echo "📁 Pasta temporária: $dir"
            else
                rm -rf "$dir"
                echo "🗑️  Pasta $dir removida!"
            fi
        fi
    done
    
    if [ "$DRY_RUN" != "true" ]; then
        echo "✅ Arquivos temporários limpos!"
    fi
}

# Função para limpar backups antigos
clean_old_backups() {
    echo "📦 Limpando backups antigos..."
    
    local backup_dirs=("backups" "backups_antes_limpeza")
    
    for dir in "${backup_dirs[@]}"; do
        if [ -d "$dir" ]; then
            if [ "$DRY_RUN" = "true" ]; then
                echo "📋 Backups antigos em $dir:"
                find "$dir" -type d -mtime +30 -ls 2>/dev/null || true
            else
                # Remover backups mais antigos que 30 dias
                find "$dir" -type d -mtime +30 -exec rm -rf {} + 2>/dev/null || true
                echo "✅ Backups antigos removidos de $dir!"
            fi
        fi
    done
}

# Função para limpeza completa
full_cleanup() {
    echo "🧹 Iniciando limpeza completa..."
    
    clean_python_cache
    clean_logs
    clean_temp_files
    clean_old_backups
    
    # Limpar arquivos de build
    echo "🔨 Limpando arquivos de build..."
    local build_patterns=("build" "dist" "*.egg-info" "*.egg")
    for pattern in "${build_patterns[@]}"; do
        if [ "$DRY_RUN" = "true" ]; then
            find . -name "$pattern" -ls 2>/dev/null || true
        else
            find . -name "$pattern" -exec rm -rf {} + 2>/dev/null || true
        fi
    done
    
    # Limpar arquivos de IDE
    echo "💻 Limpando arquivos de IDE..."
    local ide_patterns=(".vscode" ".idea" "*.swp" "*.swo")
    for pattern in "${ide_patterns[@]}"; do
        if [ "$DRY_RUN" = "true" ]; then
            find . -name "$pattern" -ls 2>/dev/null || true
        else
            find . -name "$pattern" -exec rm -rf {} + 2>/dev/null || true
        fi
    done
    
    if [ "$DRY_RUN" != "true" ]; then
        echo "✅ Limpeza completa concluída!"
    fi
}

# Função para mostrar estatísticas
show_stats() {
    echo ""
    echo "📊 Estatísticas do projeto:"
    echo "=========================="
    
    # Contar arquivos Python
    local py_files=$(find . -name "*.py" | wc -l)
    echo "🐍 Arquivos Python: $py_files"
    
    # Contar templates
    local templates=$(find templates/ -name "*.html" 2>/dev/null | wc -l)
    echo "📄 Templates HTML: $templates"
    
    # Contar arquivos estáticos
    local static_files=$(find static/ -type f 2>/dev/null | wc -l)
    echo "🎨 Arquivos estáticos: $static_files"
    
    # Tamanho do projeto
    local size=$(du -sh . | cut -f1)
    echo "📦 Tamanho total: $size"
    
    # Espaço em disco
    local disk_space=$(df -h . | tail -1 | awk '{print $4}')
    echo "💾 Espaço livre: $disk_space"
}

# Variáveis
DRY_RUN="false"
CLEAN_ALL="false"
CLEAN_CACHE="false"
CLEAN_LOGS="false"
CLEAN_TEMP="false"
CLEAN_BACKUP="false"

# Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -a|--all)
            CLEAN_ALL="true"
            shift
            ;;
        -c|--cache)
            CLEAN_CACHE="true"
            shift
            ;;
        -l|--logs)
            CLEAN_LOGS="true"
            shift
            ;;
        -t|--temp)
            CLEAN_TEMP="true"
            shift
            ;;
        -b|--backup)
            CLEAN_BACKUP="true"
            shift
            ;;
        -d|--dry-run)
            DRY_RUN="true"
            shift
            ;;
        *)
            echo "❌ Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Se nenhuma opção foi especificada, mostrar ajuda
if [ "$CLEAN_ALL" = "false" ] && [ "$CLEAN_CACHE" = "false" ] && [ "$CLEAN_LOGS" = "false" ] && [ "$CLEAN_TEMP" = "false" ] && [ "$CLEAN_BACKUP" = "false" ]; then
    echo "❌ Erro: Especifique pelo menos uma opção de limpeza!"
    echo ""
    show_help
    exit 1
fi

# Mostrar modo de execução
if [ "$DRY_RUN" = "true" ]; then
    echo "🔍 MODO SIMULAÇÃO - Nenhum arquivo será removido"
    echo ""
fi

# Executar limpeza
if [ "$CLEAN_ALL" = "true" ]; then
    full_cleanup
else
    if [ "$CLEAN_CACHE" = "true" ]; then
        clean_python_cache
    fi
    
    if [ "$CLEAN_LOGS" = "true" ]; then
        clean_logs
    fi
    
    if [ "$CLEAN_TEMP" = "true" ]; then
        clean_temp_files
    fi
    
    if [ "$CLEAN_BACKUP" = "true" ]; then
        clean_old_backups
    fi
fi

# Mostrar estatísticas
show_stats

echo ""
echo "🎉 Limpeza concluída!" 