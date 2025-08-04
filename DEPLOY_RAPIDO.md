# 🚀 DEPLOY RÁPIDO - VM

## 📋 **Passos para Deploy na VM**

### 1️⃣ **Acesse a VM**
```bash
# Via SSH ou console da VM
ssh root@10.205.109.15
```

### 2️⃣ **Navegue para o projeto**
```bash
cd /root/projet_veloz
```

### 3️⃣ **Execute o deploy**
```bash
# Opção A: Comandos manuais
git fetch origin
git reset --hard origin/main
pkill -f "python3 app.py"
nohup python3 app.py > server.log 2>&1 &

# Opção B: Script automático (se disponível)
./deploy_vm_manual.sh
```

### 4️⃣ **Verifique se está funcionando**
```bash
# Verificar se o servidor está rodando
ps aux | grep python3

# Ver logs
tail -f server.log

# Testar acesso
curl http://localhost:8001
```

## 🎯 **O que foi atualizado:**

✅ **Sistema de Metas Corrigido:**
- Cadastro de metas funcionando
- Cadastro de colaboradores funcionando  
- Cadastro de setores funcionando
- Selects carregando corretamente

✅ **Sistema de Comissões Limpo:**
- Cards zerados (R$ 0,00, 0, 0, R$ 0,00)
- Sem referências a renovação
- Interface limpa e pronta para configuração

✅ **Melhorias Gerais:**
- Script de correção automática
- Validações melhoradas
- Feedback visual aprimorado
- Interface mais intuitiva

## 🌐 **URLs para Teste:**

- **Local:** http://localhost:8001
- **VM:** http://10.205.109.15:8001
- **Metas:** http://10.205.109.15:8001/metas

## 🔧 **Comandos Úteis na VM:**

```bash
# Ver status do servidor
ps aux | grep python3

# Ver logs em tempo real
tail -f server.log

# Parar servidor
pkill -f "python3 app.py"

# Reiniciar servidor
nohup python3 app.py > server.log 2>&1 &

# Verificar porta
lsof -i :8001
```

## ✅ **Checklist de Verificação:**

- [ ] Servidor iniciado sem erros
- [ ] Acesso via http://10.205.109.15:8001
- [ ] Login funcionando
- [ ] Sistema de metas carregando
- [ ] Cadastro de colaboradores funcionando
- [ ] Cadastro de setores funcionando
- [ ] Sistema de comissões limpo

## 🚨 **Em caso de problemas:**

1. **Verificar logs:** `tail -f server.log`
2. **Reiniciar servidor:** `pkill -f "python3 app.py" && nohup python3 app.py > server.log 2>&1 &`
3. **Verificar dependências:** `pip install -r requirements.txt`
4. **Verificar porta:** `lsof -i :8001`

---

**🎉 Deploy concluído! O sistema de metas agora está funcionando perfeitamente!** 