#!/bin/bash

echo "🚀 DEPLOY PARA VM REMOTA - PROJET VELOZ"
echo "========================================="
echo ""

# Configurações
VM_IP="10.205.109.15"
VM_USER="root"
VM_PORT="22"
PROJECT_PATH="/root/projet_veloz"
REPO_URL="https://github.com/mathgallina/Projeto_atualizado.git"

echo "📋 Configurações:"
echo "   • VM IP: $VM_IP"
echo "   • Usuário: $VM_USER"
echo "   • Projeto: $PROJECT_PATH"
echo "   • Repositório: $REPO_URL"
echo ""

# Verificar se SSH está disponível
if ! command -v ssh &> /dev/null; then
    echo "❌ SSH não encontrado!"
    exit 1
fi

echo "🔍 Conectando com a VM..."
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes $VM_USER@$VM_IP "echo 'Conexão OK'" 2>/dev/null; then
    echo "❌ Não foi possível conectar com a VM!"
    echo "   Verifique se:"
    echo "   • A VM está ligada"
    echo "   • O IP está correto: $VM_IP"
    echo "   • SSH está configurado"
    exit 1
fi

echo "✅ Conexão com VM estabelecida!"

echo "🔄 Fazendo deploy na VM..."
ssh $VM_USER@$VM_IP << 'EOF'
    echo "📦 Atualizando repositório..."
    cd /root/projet_veloz
    
    # Fazer backup
    echo "📦 Criando backup..."
    cp -r app backups/app_$(date +%Y%m%d_%H%M%S)
    
    # Atualizar código
    echo "🔄 Atualizando código..."
    git fetch origin
    git reset --hard origin/main
    
    # Parar servidor se estiver rodando
    echo "🛑 Parando servidor..."
    pkill -f "python3 app.py" || true
    lsof -ti:8001 | xargs kill -9 2>/dev/null || true
    
    # Instalar dependências se necessário
    echo "📦 Verificando dependências..."
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -r requirements.txt
    
    # Iniciar servidor
    echo "🚀 Iniciando servidor..."
    nohup python3 app.py > server.log 2>&1 &
    
    echo "✅ Deploy concluído!"
    echo "🌐 Servidor disponível em: http://$VM_IP:8001"
EOF

echo ""
echo "✅ Deploy na VM concluído!"
echo "🌐 Acesse: http://$VM_IP:8001"
echo "📝 Logs do servidor: ssh $VM_USER@$VM_IP 'tail -f /root/projet_veloz/server.log'" 