# 🚀 Projet Veloz - Sistema de Gestão de Documentos

Sistema moderno de gestão de documentos com interface responsiva e funcionalidades avançadas.

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução](#execução)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Deploy e Rollback](#deploy-e-rollback)
- [Desenvolvimento](#desenvolvimento)
- [Troubleshooting](#troubleshooting)

## ✨ Características

- 🔐 **Sistema de Autenticação**: Login seguro com bcrypt
- 📄 **Gestão de Documentos**: Upload, edição e categorização
- 📊 **Dashboard Interativo**: Cards com estatísticas em tempo real
- 🔔 **Sistema de Notificações**: Alertas e notificações em tempo real
- 📈 **Analytics**: Relatórios e métricas de uso
- 🔄 **Sistema de Backup**: Backup automático para Google Drive
- 📱 **Interface Responsiva**: Design moderno para desktop e mobile
- 🎨 **UI/UX Moderna**: Gradientes, animações e efeitos visuais

## 🛠️ Requisitos

- Python 3.9+
- pip
- Git
- Navegador web moderno

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd projet_veloz
```

### 2. Crie e ative o ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
PORT=8001
```

### Configuração do Google Drive (Opcional)
Para usar o sistema de backup automático:

```env
GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json
GOOGLE_DRIVE_TOKEN_FILE=token.json
```

## 🏃‍♂️ Execução

### Método 1: Script Automático (Recomendado)
```bash
chmod +x start_server.sh
./start_server.sh
```

### Método 2: Execução Manual
```bash
source .venv/bin/activate
python app.py
```

### Acesso ao Sistema
- **URL**: http://localhost:8001
- **Login**: admin
- **Senha**: admin123

## 📁 Estrutura do Projeto

```
projet_veloz/
├── app/                    # Código principal da aplicação
│   ├── core/              # Configurações e database
│   ├── modules/           # Módulos da aplicação
│   │   ├── auth/         # Autenticação
│   │   ├── documents/    # Gestão de documentos
│   │   ├── analytics/    # Analytics e relatórios
│   │   ├── backup/       # Sistema de backup
│   │   └── ...
│   ├── shared/           # Utilitários compartilhados
│   ├── static/           # Arquivos estáticos
│   └── templates/        # Templates HTML
├── tests/                # Testes automatizados
├── logs/                 # Logs da aplicação
├── backups/              # Backups locais
├── docs/                 # Documentação
├── scripts/              # Scripts utilitários
├── app.py               # Ponto de entrada
├── requirements.txt      # Dependências Python
└── README.md           # Este arquivo
```

## 🔄 Deploy e Rollback

### Deploy em Produção

1. **Preparar o servidor**:
```bash
git clone <repositorio>
cd projet_veloz
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Configurar variáveis de produção**:
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY=<chave-secreta-producao>
```

3. **Executar com Gunicorn**:
```bash
gunicorn -w 4 -b 0.0.0.0:8001 app:app
```

### Rollback Seguro

#### Script de Rollback Automático
```bash
#!/bin/bash
# rollback.sh

echo "🔄 Iniciando rollback..."

# Fazer backup do estado atual
git stash

# Voltar para o último commit estável
git reset --hard HEAD~1

# Reinstalar dependências se necessário
pip install -r requirements.txt

# Reiniciar o servidor
pkill -f "python app.py"
python app.py &

echo "✅ Rollback concluído!"
```

#### Rollback Manual
```bash
# Ver commits disponíveis
git log --oneline

# Fazer rollback para commit específico
git reset --hard <commit-hash>

# Ou voltar para tag específica
git checkout <tag-name>
```

### Tags de Versão
```bash
# Criar tag para versão
git tag -a v1.0.0 -m "Versão 1.0.0 - Estável"

# Fazer push das tags
git push origin --tags

# Voltar para versão específica
git checkout v1.0.0
```

## 🛠️ Desenvolvimento

### Branches
- `main`: Código de produção estável
- `dev`: Desenvolvimento e testes
- `feature/*`: Novas funcionalidades
- `hotfix/*`: Correções urgentes

### Workflow de Desenvolvimento
```bash
# Criar branch para nova feature
git checkout -b feature/nova-funcionalidade

# Desenvolver e commitar
git add .
git commit -m "feat: adiciona nova funcionalidade"

# Fazer merge para dev
git checkout dev
git merge feature/nova-funcionalidade

# Fazer merge para main após testes
git checkout main
git merge dev
```

### Testes
```bash
# Executar testes
python -m pytest tests/

# Executar com coverage
python -m pytest --cov=app tests/
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Porta 8001 já em uso
```bash
# Encontrar processo usando a porta
lsof -i :8001

# Matar processo
kill -9 <PID>
```

#### 2. Erro de dependências
```bash
# Reinstalar dependências
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

#### 3. Erro de permissões
```bash
# Dar permissão aos scripts
chmod +x *.sh
```

#### 4. Ambiente virtual não ativado
```bash
# Verificar se está ativado
which python
# Deve mostrar: /path/to/projet_veloz/.venv/bin/python
```

### Logs
- **Logs da aplicação**: `logs/app.log`
- **Logs de erro**: `logs/error.log`
- **Logs de acesso**: `logs/access.log`

## 📞 Suporte

- **Documentação**: Consulte a pasta `docs/`
- **Issues**: Abra uma issue no GitHub
- **Email**: suporte@projetveloz.com

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**⚠️ IMPORTANTE**: O sistema SEMPRE roda na porta 8001. Não altere esta configuração! 