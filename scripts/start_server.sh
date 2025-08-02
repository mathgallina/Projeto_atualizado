#!/bin/bash

echo "🚀 SISTEMA VELOZ FIBRA - VERSÃO MELHORADA!"
echo "=============================================="
echo ""
echo "✅ Sistema restaurado ao estado original"
echo "✅ Interface modernizada e responsiva"
echo "✅ Dashboard com cards interativos"
echo "✅ Login com design profissional"
echo "✅ Efeitos visuais e animações"
echo ""
echo "🌐 Acesse: http://localhost:8001"
echo "👤 Login: admin"
echo "🔑 Senha: admin123"
echo ""
echo "🎨 Melhorias implementadas:"
echo "   • Design moderno com gradientes"
echo "   • Cards interativos com hover effects"
echo "   • Header com navegação"
echo "   • Botões de ação rápida"
echo "   • Login com efeitos visuais"
echo "   • Responsivo para mobile"
echo ""
echo "🔥 Iniciando servidor..."

# Verificar se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativar ambiente virtual
source .venv/bin/activate

# Verificar se as dependências estão instaladas
if [ ! -f ".venv/lib/python*/site-packages/flask" ]; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
fi

# Verificar se a porta 8001 está livre
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Porta 8001 já está em uso!"
    echo "🔄 Matando processo na porta 8001..."
    lsof -ti:8001 | xargs kill -9
fi

# Iniciar servidor
echo "🚀 Servidor iniciando na porta 8001..."
python3 app.py 