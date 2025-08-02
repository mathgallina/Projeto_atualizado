# Regras Oficiais de Desenvolvimento - Projet_Veloz

## Status de Conformidade ✅

**Data de Verificação:** $(date)
**Versão Atual:** 1.0.0 (Base Estável)
**Status:** CONFORME

---

## 1. Versão Base e Controle de Versão ✅

### Regras:
- ✅ Versão 1.0.0 é a base estável e referência
- ✅ Rollback para 1.0.0 em caso de problemas graves
- ✅ Novas funcionalidades em versões incrementais: 1.0.1, 1.0.2, 1.1.0
- ✅ Nunca modificar diretamente a versão 1.0.0

### Implementação:
- Sistema de versionamento Git implementado
- Tags de versão disponíveis
- Documentação de rollback em `docs/`

---

## 2. Ambiente e Porta ✅

### Regras:
- ✅ Sistema deve rodar na porta 8001, sem exceções
- ✅ Qualquer alteração na porta é proibida

### Implementação:
- Porta fixa configurada em `app.py` linha 13
- Configuração: `port = int(os.environ.get("PORT", 8001))`
- Comentário explicativo: "Porta fixa 8001 para projet_veloz"

---

## 3. Organização de Código ✅

### Regras:
- ✅ Código separado e organizado em pastas claras
- ✅ Comentários claros e código modular obrigatórios

### Estrutura Implementada:
```
projet_veloz/
├── app/                    # Backend e lógica
│   ├── core/              # Configurações centrais
│   ├── modules/           # Módulos organizados
│   ├── shared/            # Utilitários compartilhados
│   └── static/            # Arquivos estáticos
├── templates/             # Front-end HTML
├── static/               # CSS, JS, imagens
├── scripts/              # Automações e deploy
├── docs/                 # Documentação
└── tests/                # Testes
```

### Qualidade do Código:
- ✅ Comentários claros em todos os arquivos principais
- ✅ Código modular com separação de responsabilidades
- ✅ Configuração centralizada em `app/core/config.py`

---

## 4. Processos de Desenvolvimento ✅

### Regras:
- ✅ Alterações em branch específica
- ✅ Commits pequenos, claros e frequentes
- ✅ Pull requests obrigatórios
- ✅ Testes completos antes de deploy

### Implementação:
- Scripts de automação em `scripts/`
- Makefile para comandos padronizados
- Configuração de testes em `pytest.ini`

---

## 5. Proteção e Backup ✅

### Regras:
- ✅ Repositório Git atualizado com tags
- ✅ Documentação de rollback disponível
- ✅ Backups automáticos regulares

### Implementação:
- Sistema de backup em `app/modules/backup/`
- Integração com Google Drive
- Retenção configurável de backups
- Scripts de rollback em `scripts/rollback.sh`

---

## 6. Dependências e Versões ✅

### Requirements.txt Atual:
```
Flask==2.3.3
Flask-CORS==4.0.0
markdown==3.5.1
python-slugify==8.0.1
Werkzeug==2.3.7
gunicorn==21.2.0
Flask-Login==0.6.3
Flask-WTF==1.1.1
WTForms==3.0.1
bcrypt==4.0.1
python-dotenv==1.0.0
# Backup System Dependencies
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
cryptography==41.0.7
schedule==1.2.0
zipfile36==0.1.3
```

### Status:
- ✅ Versões fixas para estabilidade
- ✅ Dependências organizadas por categoria
- ✅ Comentários explicativos

---

## 7. Responsabilidades do Cursor ✅

### Regras:
- ✅ Gerar código seguindo regras sem exceções
- ✅ Alertar sobre riscos de quebra
- ✅ Documentar mudanças com clareza
- ✅ Garantir estrutura e funcionalidade

### Implementação:
- Documentação completa em `docs/`
- Guias de uso em `docs/GUIA_USO_SISTEMA.md`
- Relatórios de mudanças mantidos

---

## Checklist de Conformidade

- [x] Versão base 1.0.0 preservada
- [x] Porta 8001 fixa e documentada
- [x] Estrutura de pastas organizada
- [x] Código modular e comentado
- [x] Processos de desenvolvimento definidos
- [x] Sistema de backup implementado
- [x] Dependências versionadas
- [x] Documentação atualizada

---

## Próximas Ações

1. **Monitoramento Contínuo:**
   - Verificar conformidade antes de cada commit
   - Atualizar documentação conforme mudanças
   - Manter backup da versão 1.0.0

2. **Desenvolvimento Seguro:**
   - Sempre criar branches para novas funcionalidades
   - Testar completamente antes de merge
   - Documentar todas as mudanças

3. **Revisão Periódica:**
   - Revisar este documento mensalmente
   - Atualizar conforme evolução do projeto
   - Manter histórico de mudanças

---

**Última Atualização:** $(date)
**Próxima Revisão:** $(date -d "+1 month")
**Responsável:** Equipe de Desenvolvimento Projet_Veloz 