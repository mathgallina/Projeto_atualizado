# 🚀 INSTRUÇÕES PARA ATUALIZAR A VM

## Problema
A VM (10.205.109.15:8001) ainda está mostrando os dados antigos de renovação porque não foi atualizada com as mudanças que fizemos.

## Solução

### Opção 1: Executar script na VM (Recomendado)

1. **Acesse a VM** via SSH ou console
2. **Navegue para o diretório do projeto:**
   ```bash
   cd /root/projet_veloz
   ```

3. **Execute o script de atualização:**
   ```bash
   ./update_vm.sh
   ```

### Opção 2: Comandos manuais na VM

Se o script não funcionar, execute estes comandos na VM:

```bash
# 1. Ir para o diretório do projeto
cd /root/projet_veloz

# 2. Fazer backup
mkdir -p backups
cp -r app backups/app_$(date +%Y%m%d_%H%M%S)

# 3. Atualizar código
git fetch origin
git reset --hard origin/main

# 4. Parar servidor
pkill -f "python3 app.py" || true
lsof -ti:8001 | xargs kill -9 2>/dev/null || true

# 5. Verificar dependências
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

# 6. Iniciar servidor
nohup python3 app.py > server.log 2>&1 &

# 7. Verificar se está funcionando
curl http://localhost:8001
```

### Opção 3: Copiar arquivo atualizado

Se não conseguir acessar a VM via SSH, você pode:

1. **Copiar o arquivo atualizado** `app/templates/metas.html` para a VM
2. **Substituir o arquivo** na VM: `/root/projet_veloz/app/templates/metas.html`
3. **Reiniciar o servidor** na VM

## Verificação

Após a atualização, acesse:
- **http://10.205.109.15:8001/metas**
- Vá na aba "Comissões"
- Você deve ver:
  - Cards zerados (R$ 0,00, 0, 0, R$ 0,00)
  - Sem referências a "renovação"
  - Tipos de comissão limpos

## Logs do Servidor

Para ver os logs do servidor na VM:
```bash
tail -f /root/projet_veloz/server.log
```

## Backup

O backup será criado em:
```bash
/root/projet_veloz/backups/app_YYYYMMDD_HHMMSS/
```

---

**Nota:** As mudanças já estão no repositório Git e funcionando localmente. Só precisamos atualizar a VM para que ela use a versão mais recente do código. 