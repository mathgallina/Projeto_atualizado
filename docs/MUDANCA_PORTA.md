# 🔄 MUDANÇA DE PORTA - SISTEMA VELOZ FIBRA

## ✅ Alteração Realizada

### 📍 **Porta Alterada:**
- **Antes:** Porta 8000
- **Depois:** Porta 8001

### 🔧 **Arquivos Modificados:**

1. **`app.py`**
   ```python
   # Antes:
   port = int(os.environ.get("PORT", 8000))
   
   # Depois:
   port = int(os.environ.get("PORT", 8001))
   ```

2. **`rodar_sistema_original.sh`**
   - URL atualizada para http://localhost:8001

3. **`GUIA_USO_SISTEMA.md`**
   - URLs atualizadas para porta 8001

4. **`start_server.sh`** (novo)
   - Script de inicialização na porta 8001

## 🚀 Como Usar

### **Opção 1 - Script automático:**
```bash
./start_server.sh
```

### **Opção 2 - Manual:**
```bash
source .venv/bin/activate
python3 app.py
```

### **Opção 3 - Script original:**
```bash
./rodar_sistema_original.sh
```

## 🌐 Acessar o Sistema

- **URL Principal:** http://localhost:8001
- **Login:** admin
- **Senha:** admin123

## ✅ Status Atual

- ✅ Servidor rodando na porta 8001
- ✅ Sistema funcionando corretamente
- ✅ Interface modernizada
- ✅ Dashboard interativo
- ✅ Login funcional

## 🔍 Verificação

Para verificar se o servidor está rodando:
```bash
lsof -i :8001
curl http://localhost:8001
```

---

🎉 **Sistema funcionando na porta 8001!** 