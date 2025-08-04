#!/bin/bash

echo "🚀 DEPLOY MANUAL PARA VM - PROJET VELOZ"
echo "========================================"
echo ""

echo "📋 Instruções:"
echo "1. Copie este script para a VM"
echo "2. Execute: chmod +x deploy_vm_manual.sh"
echo "3. Execute: ./deploy_vm_manual.sh"
echo ""

# Configurações
PROJECT_PATH="/root/projet_veloz"
REPO_URL="https://github.com/mathgallina/Projeto_atualizado.git"

echo "🔍 Verificando ambiente..."
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ Diretório do projeto não encontrado: $PROJECT_PATH"
    echo "   Verifique se o caminho está correto"
    exit 1
fi

cd "$PROJECT_PATH"

echo "📦 Criando backup..."
mkdir -p backups
cp -r app backups/app_$(date +%Y%m%d_%H%M%S)

echo "🔄 Atualizando código..."
git fetch origin
git reset --hard origin/main

echo "🛑 Parando servidor..."
pkill -f "python3 app.py" || true
lsof -ti:8001 | xargs kill -9 2>/dev/null || true

echo "📦 Verificando dependências..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

echo "🚀 Iniciando servidor..."
nohup python3 app.py > server.log 2>&1 &

echo ""
echo "✅ Deploy concluído!"
echo "🌐 Servidor disponível em: http://10.205.109.15:8001"
echo "📝 Logs do servidor: tail -f server.log"
echo ""
echo "🎯 Melhorias aplicadas:"
echo "   • Sistema de metas corrigido"
echo "   • Cadastro de colaboradores funcionando"
echo "   • Cadastro de setores funcionando"
echo "   • Sistema de comissões limpo"
echo "   • Interface simplificada" 