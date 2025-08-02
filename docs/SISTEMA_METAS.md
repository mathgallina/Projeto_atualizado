# Sistema de Metas - Veloz Fibra

## Visão Geral

O Sistema de Metas é um módulo completo integrado ao projeto Veloz Fibra que permite gerenciar metas e objetivos de forma eficiente, com controle por colaboradores e setores.

## Funcionalidades

### 1. Dashboard Principal
- **Card "Sistema de Metas"**: Substitui o card "Tecnologia de Ponta" na página principal
- **Redirecionamento**: Ao clicar no card, redireciona para `/goals`
- **Design**: Mantém o padrão visual escuro com gradiente roxo/azul

### 2. Página do Sistema de Metas (`/goals`)

#### Indicadores Principais
- **Total de Metas**: Número total de metas cadastradas
- **Metas Concluídas**: Metas com status "concluído"
- **Metas Atrasadas**: Metas que passaram da data de vencimento
- **Metas Ativas**: Metas em andamento

#### Funcionalidades
- **Listagem de Metas**: Cards individuais com informações completas
- **Busca**: Pesquisa por título, descrição ou colaborador
- **Criação**: Modal para adicionar novas metas
- **Edição**: Modal para editar metas existentes
- **Exclusão**: Botão para deletar metas
- **Status**: Indicadores visuais de status (Ativo, Concluído, Atrasado)

### 3. Gestão de Colaboradores
- **Cadastro**: Nome completo, setor, email, telefone
- **Associação**: Vinculação automática com setores
- **Seleção**: Dropdown para escolha em metas

### 4. Gestão de Setores
- **Setores Padrão**: Comercial, Técnico, Financeiro, RH, TI, Marketing
- **Personalização**: Possibilidade de adicionar novos setores
- **Cores e Ícones**: Identificação visual por setor

## Estrutura Técnica

### Backend (Flask)

#### Módulos
```
app/modules/goals/
├── __init__.py
├── models.py              # Modelos de dados
├── routes.py              # Rotas e endpoints
├── repositories/          # Acesso a dados
│   ├── __init__.py
│   ├── goals_repository.py
│   ├── collaborators_repository.py
│   └── sectors_repository.py
└── services/             # Lógica de negócio
    ├── __init__.py
    ├── goals_service.py
    ├── collaborators_service.py
    └── sectors_service.py
```

#### Modelos de Dados
- **Goal**: Meta com título, descrição, colaborador, setor, data de vencimento, status
- **Collaborator**: Colaborador com nome, setor, contatos
- **Sector**: Setor com nome, descrição, cor, ícone

#### Status das Metas
- **Ativo**: Meta em andamento
- **Concluído**: Meta finalizada
- **Atrasado**: Meta que passou da data de vencimento

### Frontend (HTML/CSS/JavaScript)

#### Templates
- **Página Principal**: `app/templates/main/index.html` (card atualizado)
- **Sistema de Metas**: `app/templates/goals/index.html`

#### Funcionalidades JavaScript
- **Modais**: Criação e edição de metas e colaboradores
- **API Calls**: Comunicação com endpoints REST
- **Busca**: Filtragem em tempo real
- **Validação**: Verificação de campos obrigatórios

## API Endpoints

### Metas
- `GET /goals/api/goals` - Listar todas as metas
- `GET /goals/api/goals/<id>` - Obter meta específica
- `POST /goals/api/goals` - Criar nova meta
- `PUT /goals/api/goals/<id>` - Atualizar meta
- `DELETE /goals/api/goals/<id>` - Deletar meta
- `PUT /goals/api/goals/<id>/status` - Atualizar status
- `GET /goals/api/goals/statistics` - Estatísticas

### Colaboradores
- `GET /goals/api/collaborators` - Listar colaboradores
- `POST /goals/api/collaborators` - Criar colaborador
- `PUT /goals/api/collaborators/<id>` - Atualizar colaborador
- `DELETE /goals/api/collaborators/<id>` - Deletar colaborador
- `GET /goals/api/collaborators/select` - Lista para select

### Setores
- `GET /goals/api/sectors` - Listar setores
- `POST /goals/api/sectors` - Criar setor
- `PUT /goals/api/sectors/<id>` - Atualizar setor
- `DELETE /goals/api/sectors/<id>` - Deletar setor
- `GET /goals/api/sectors/select` - Lista para select

## Persistência de Dados

### Arquivos JSON
- `app/data/goals.json` - Dados das metas
- `app/data/collaborators.json` - Dados dos colaboradores
- `app/data/sectors.json` - Dados dos setores

### Estrutura de Dados
```json
{
  "id": "unique-id",
  "title": "Título da Meta",
  "description": "Descrição opcional",
  "collaborator_id": "id-do-colaborador",
  "sector_id": "id-do-setor",
  "due_date": "2025-02-15T23:59:59",
  "status": "ativo|concluido|atrasado",
  "created_at": "2025-01-20T10:00:00",
  "updated_at": "2025-01-20T10:00:00"
}
```

## Navegação

### Fluxo Principal
1. **Dashboard Principal** (`/`) → Card "Sistema de Metas"
2. **Sistema de Metas** (`/goals`) → Página completa de gestão
3. **Menu Lateral** → Navegação entre seções

### Integração
- **Autenticação**: Todas as rotas requerem login
- **Padrão Visual**: Mantém identidade visual escura
- **Responsividade**: Design adaptável para diferentes telas

## Configuração

### Registro do Blueprint
O módulo é registrado automaticamente em `app/__init__.py`:
```python
from app.modules.goals.routes import goals_bp
app.register_blueprint(goals_bp, url_prefix="/goals")
```

### Dados Iniciais
- **Setores**: Inicializados automaticamente com setores padrão
- **Colaboradores**: Arquivo de exemplo com 5 colaboradores
- **Metas**: Arquivo de exemplo com 6 metas

## Testes

### Acesso ao Sistema
1. Acesse `http://localhost:8001`
2. Faça login (usuário padrão: admin/admin)
3. Clique no card "Sistema de Metas"
4. Explore as funcionalidades

### Funcionalidades para Testar
- ✅ Visualizar indicadores
- ✅ Criar nova meta
- ✅ Criar novo colaborador
- ✅ Editar meta existente
- ✅ Deletar meta
- ✅ Buscar metas
- ✅ Filtrar por status

## Escalabilidade

### Melhorias Futuras
- **Notificações**: Alertas para metas próximas do vencimento
- **Relatórios**: Exportação de dados em PDF/Excel
- **Dashboard**: Gráficos e métricas avançadas
- **Permissões**: Controle de acesso por setor
- **Histórico**: Log de alterações nas metas
- **Comentários**: Sistema de comentários nas metas

### Arquitetura
- **Modular**: Fácil adição de novas funcionalidades
- **Extensível**: Padrão CDD v2.0 mantido
- **Manutenível**: Código bem documentado e organizado

## Autor

**Matheus Gallina** - Desenvolvedor Full Stack
- **Versão**: 1.0.0
- **Data**: Janeiro 2025
- **Licença**: MIT 