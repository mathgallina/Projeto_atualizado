# 🛡️ ISOLAMENTO DO SISTEMA RH - PROJETO VELOZ FIBRA

## 📋 Visão Geral

Este documento descreve as regras e estrutura de isolamento do sistema de RH no projeto VELOZ FIBRA, garantindo que funcionalidades existentes não sejam afetadas.

## 🎯 Objetivos do Isolamento

1. **Proteger funcionalidades existentes** - Páginas principais e documentos corporativos não devem sofrer interferência
2. **Isolamento total** - Sistema RH em rota exclusiva `/rh`
3. **Blueprint exclusivo** - Estrutura própria em `app/modules/rh/`
4. **Navegação limpa** - Apenas links visuais para `/rh` sem scripts ou handlers
5. **Porta fixa** - Manter porta 8001 para toda aplicação

## 🏗️ Estrutura de Isolamento

### 📁 Estrutura de Arquivos

```
app/
├── modules/
│   └── rh/                    # 🛡️ SISTEMA RH ISOLADO
│       ├── __init__.py
│       ├── routes.py          # Rotas exclusivas /rh/*
│       ├── models.py          # Modelos RH
│       ├── services/          # Serviços RH
│       ├── repositories/      # Repositórios RH
│       └── templates/         # Templates RH isolados
├── templates/
│   ├── index.html            # 🚫 SEM CÓDIGO RH
│   ├── documents/            # 🚫 SEM CÓDIGO RH
│   └── main/                 # 🚫 SEM CÓDIGO RH
└── data/
    ├── employees.json        # 📊 Dados RH isolados
    ├── equipment.json        # 📊 Dados RH isolados
    └── corporate_documents.json # 📊 Dados RH isolados
```

### 🔒 Regras de Isolamento

#### 1. **Rotas Exclusivas**
- ✅ Todas as rotas RH começam com `/rh`
- ✅ Blueprint registrado com `url_prefix="/rh"`
- ✅ Nenhuma rota RH fora do blueprint

#### 2. **Templates Isolados**
- ✅ Templates RH em `app/templates/rh/`
- ✅ Nenhum template RH em outras pastas
- ✅ Comentários de blindagem em todos os arquivos RH

#### 3. **Dados Isolados**
- ✅ Arquivos JSON RH separados
- ✅ Nenhuma interferência com dados existentes
- ✅ Estrutura de dados própria

#### 4. **Navegação Limpa**
- ✅ Links visuais simples para `/rh`
- ✅ Sem JavaScript RH em páginas principais
- ✅ Sem modais ou handlers RH externos

## 🚫 Áreas Protegidas

### 📄 Páginas Principais (PROTEGIDAS)
- `/` - Dashboard principal
- `/documents` - Gestão de documentos
- `/pages` - Páginas do sistema
- `/admin/*` - Área administrativa

### 🛡️ Sistema RH (ISOLADO)
- `/rh/` - Dashboard RH
- `/rh/employees` - Funcionários
- `/rh/equipment` - Equipamentos
- `/rh/documents` - Documentos RH
- `/rh/search` - Busca RH
- `/rh/reports` - Relatórios RH

## 📝 Comentários de Blindagem

Todos os arquivos do sistema RH devem conter:

```html
<!--
Página blindada: não adicionar JS, modais ou handlers do sistema RH aqui.
Qualquer alteração deve ser aprovada.
-->
```

```python
"""
Sistema RH isolado: não adicionar código que afete outras funcionalidades.
Qualquer alteração deve ser aprovada.
"""
```

## 🔧 Configuração do Blueprint

### Registro no `app/__init__.py`

```python
try:
    # Register RH module
    from app.modules.rh.routes import rh_bp
    app.register_blueprint(rh_bp, url_prefix="/rh")
    logger.info("RH blueprint registered")
except Exception as e:
    logger.error(f"Error registering RH blueprint: {e}")
```

### Estrutura do Blueprint

```python
from flask import Blueprint

rh_bp = Blueprint('rh', __name__, url_prefix='/rh')

@rh_bp.route('/')
def index():
    """Dashboard RH isolado"""
    return render_template('rh/index.html')
```

## 🎨 Navegação e Interface

### Links Visuais na Home

```html
<!-- Link visual simples para RH -->
<a href="/rh/" class="card-hover">
    <div class="gradient-rh">
        <i class="fas fa-users"></i>
        <h3>Setor RH</h3>
        <p>Acesso a documentos, políticas e comunicações do RH</p>
    </div>
</a>
```

### Menu Lateral RH

```html
<!-- Menu isolado do RH -->
<nav class="space-y-2">
    <a href="/rh/" class="nav-item">Dashboard</a>
    <a href="/rh/employees" class="nav-item">Funcionários</a>
    <a href="/rh/equipment" class="nav-item">Equipamentos</a>
    <a href="/rh/documents" class="nav-item">Documentos</a>
</nav>
```

## 🧪 Testes de Isolamento

### ✅ Testes Obrigatórios

1. **Navegação Principal**
   - ✅ Acesso a `/` sem interferência
   - ✅ Acesso a `/documents` sem interferência
   - ✅ Acesso a `/pages` sem interferência

2. **Navegação RH**
   - ✅ Acesso a `/rh/` funcionando
   - ✅ Todas as rotas `/rh/*` funcionando
   - ✅ Navegação interna RH funcionando

3. **Isolamento de Dados**
   - ✅ Dados RH não afetam dados principais
   - ✅ Dados principais não afetam RH
   - ✅ Estruturas de dados separadas

4. **Interface**
   - ✅ Links visuais funcionando
   - ✅ Sem JavaScript conflitante
   - ✅ Sem modais interferindo

## 🚨 Regras de Desenvolvimento

### ❌ PROIBIDO

1. **Adicionar código RH em páginas principais**
2. **Modificar templates existentes para incluir RH**
3. **Criar rotas RH fora do blueprint**
4. **Misturar dados RH com dados principais**
5. **Adicionar JavaScript RH em páginas não-RH**

### ✅ PERMITIDO

1. **Desenvolver dentro do blueprint RH**
2. **Criar templates em `app/templates/rh/`**
3. **Usar dados isolados em `app/data/`**
4. **Adicionar links visuais simples**
5. **Implementar funcionalidades RH completas**

## 📊 Monitoramento

### Logs de Isolamento

```python
logger.info("RH blueprint registered - ISOLATED")
logger.info("RH templates loaded - ISOLATED")
logger.info("RH data initialized - ISOLATED")
```

### Verificação de Integridade

- ✅ Blueprint registrado corretamente
- ✅ Templates isolados
- ✅ Dados separados
- ✅ Navegação limpa
- ✅ Sem conflitos detectados

## 🔄 Manutenção

### Atualizações

1. **Sempre testar isolamento após mudanças**
2. **Verificar se não há interferência**
3. **Manter documentação atualizada**
4. **Comentar alterações importantes**

### Rollback

1. **Reverter mudanças se houver interferência**
2. **Restaurar backup se necessário**
3. **Testar funcionalidades principais**
4. **Documentar problemas encontrados**

---

**⚠️ IMPORTANTE**: Este isolamento é CRÍTICO para a estabilidade do sistema. Qualquer alteração deve ser testada rigorosamente antes de ser implementada.

**📅 Última atualização**: 02/08/2025
**🔒 Status**: ISOLAMENTO ATIVO
**✅ Testado**: SIM 