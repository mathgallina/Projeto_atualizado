#!/bin/bash

echo "🔧 INICIALIZAÇÃO DO GIT - PROJET VELOZ"
echo "======================================="
echo ""

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Opções:"
    echo "  -h, --help          Mostra esta ajuda"
    echo "  -r, --remote URL    Configurar repositório remoto"
    echo "  -b, --branch BRANCH Branch inicial (padrão: main)"
    echo "  -t, --tag           Criar tag inicial v1.0.0"
    echo "  -c, --commit        Fazer commit inicial"
    echo ""
    echo "Exemplos:"
    echo "  $0                    # Inicialização básica"
    echo "  $0 -r https://github.com/user/projet_veloz.git"
    echo "  $0 -b dev -t         # Branch dev + tag"
    echo "  $0 -c -r https://github.com/user/projet_veloz.git"
}

# Função para inicializar Git
init_git() {
    echo "🔧 Inicializando repositório Git..."
    
    if [ -d ".git" ]; then
        echo "ℹ️  Repositório Git já existe."
        return
    fi
    
    git init
    echo "✅ Repositório Git inicializado!"
}

# Função para configurar Git
setup_git() {
    echo "⚙️  Configurando Git..."
    
    # Configurar usuário se não estiver configurado
    if [ -z "$(git config user.name)" ]; then
        echo "👤 Configurando usuário Git..."
        read -p "Nome do usuário: " user_name
        read -p "Email do usuário: " user_email
        
        git config user.name "$user_name"
        git config user.email "$user_email"
    fi
    
    # Configurar branch padrão
    git config init.defaultBranch main
    
    echo "✅ Git configurado!"
}

# Função para adicionar arquivos
add_files() {
    echo "📁 Adicionando arquivos ao Git..."
    
    # Adicionar todos os arquivos exceto os ignorados
    git add .
    
    # Verificar se há arquivos para commitar
    if git diff --cached --quiet; then
        echo "ℹ️  Nenhum arquivo para commitar."
        return 1
    fi
    
    echo "✅ Arquivos adicionados!"
    return 0
}

# Função para fazer commit inicial
make_initial_commit() {
    echo "💾 Fazendo commit inicial..."
    
    if add_files; then
        git commit -m "feat: commit inicial do projet_veloz

- Sistema de gestão de documentos
- Interface moderna e responsiva
- Sistema de autenticação
- Dashboard interativo
- Sistema de backup automático
- Configuração organizada e limpa"
        
        echo "✅ Commit inicial criado!"
        return 0
    else
        echo "ℹ️  Nenhum commit necessário."
        return 1
    fi
}

# Função para configurar repositório remoto
setup_remote() {
    local remote_url="$1"
    
    echo "🌐 Configurando repositório remoto..."
    
    # Verificar se já existe um remote
    if git remote get-url origin &>/dev/null; then
        echo "🔄 Atualizando remote origin..."
        git remote set-url origin "$remote_url"
    else
        echo "➕ Adicionando remote origin..."
        git remote add origin "$remote_url"
    fi
    
    echo "✅ Repositório remoto configurado!"
}

# Função para criar branch
create_branch() {
    local branch="$1"
    
    echo "🌿 Criando branch: $branch"
    
    # Verificar se já estamos na branch desejada
    current_branch=$(git branch --show-current)
    if [ "$current_branch" = "$branch" ]; then
        echo "ℹ️  Já estamos na branch $branch"
        return
    fi
    
    # Criar e mudar para a branch
    git checkout -b "$branch"
    echo "✅ Branch $branch criada e ativada!"
}

# Função para criar tag
create_tag() {
    echo "🏷️  Criando tag v1.0.0..."
    
    git tag -a v1.0.0 -m "Versão 1.0.0 - Release inicial

- Sistema completo de gestão de documentos
- Interface moderna e responsiva
- Sistema de autenticação seguro
- Dashboard interativo
- Backup automático configurado
- Estrutura organizada e limpa"
    
    echo "✅ Tag v1.0.0 criada!"
}

# Função para fazer push
push_to_remote() {
    local branch="$1"
    
    echo "📤 Fazendo push para o repositório remoto..."
    
    # Fazer push da branch atual
    git push -u origin "$branch"
    
    # Fazer push das tags se existirem
    if git tag -l | grep -q .; then
        git push origin --tags
    fi
    
    echo "✅ Push concluído!"
}

# Função para mostrar status
show_status() {
    echo ""
    echo "📊 Status do repositório:"
    echo "========================="
    
    echo "🌿 Branch atual: $(git branch --show-current)"
    echo "📝 Último commit: $(git log -1 --oneline)"
    echo "🏷️  Tags: $(git tag -l | tr '\n' ' ')"
    
    if git remote get-url origin &>/dev/null; then
        echo "🌐 Remote: $(git remote get-url origin)"
    else
        echo "🌐 Remote: Não configurado"
    fi
    
    echo ""
    echo "📋 Arquivos modificados:"
    git status --short
}

# Variáveis
REMOTE_URL=""
BRANCH="main"
CREATE_TAG="false"
MAKE_COMMIT="false"

# Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -r|--remote)
            REMOTE_URL="$2"
            shift 2
            ;;
        -b|--branch)
            BRANCH="$2"
            shift 2
            ;;
        -t|--tag)
            CREATE_TAG="true"
            shift
            ;;
        -c|--commit)
            MAKE_COMMIT="true"
            shift
            ;;
        *)
            echo "❌ Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

echo "🚀 Iniciando configuração do Git..."
echo ""

# Executar etapas
init_git
setup_git

if [ "$MAKE_COMMIT" = "true" ]; then
    make_initial_commit
fi

if [ -n "$BRANCH" ] && [ "$BRANCH" != "main" ]; then
    create_branch "$BRANCH"
fi

if [ "$CREATE_TAG" = "true" ]; then
    create_tag
fi

if [ -n "$REMOTE_URL" ]; then
    setup_remote "$REMOTE_URL"
    
    # Fazer push se houver commits
    if git rev-parse HEAD &>/dev/null; then
        push_to_remote "$BRANCH"
    fi
fi

# Mostrar status final
show_status

echo ""
echo "🎉 Configuração do Git concluída!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Configure seu repositório remoto no GitHub/GitLab"
echo "   2. Execute: git remote add origin <URL_DO_REPOSITORIO>"
echo "   3. Execute: git push -u origin $BRANCH"
echo "   4. Configure GitHub Actions para CI/CD (opcional)" 