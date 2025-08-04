// SISTEMA DE METAS - CORREÇÕES E MELHORIAS
// ===========================================

// Funções de correção para o sistema de metas
window.metasFix = {
    
    // Corrigir carregamento de setores nos selects
    fixSectorSelects: function() {
        console.log('🔧 Corrigindo selects de setores...');
        
        // Corrigir select de metas
        const goalSectorSelect = document.getElementById('goalSector');
        if (goalSectorSelect) {
            goalSectorSelect.innerHTML = '<option value="">Selecione o setor</option>';
            window.metasApp.sectors.forEach(sector => {
                const option = document.createElement('option');
                option.value = sector.id;
                option.textContent = sector.name;
                goalSectorSelect.appendChild(option);
            });
        }
        
        // Corrigir select de colaboradores
        const collaboratorSectorSelect = document.querySelector('select[x-model="newCollaborator.sectorId"]');
        if (collaboratorSectorSelect) {
            collaboratorSectorSelect.innerHTML = '<option value="">Selecione o setor</option>';
            window.metasApp.sectors.forEach(sector => {
                const option = document.createElement('option');
                option.value = sector.id;
                option.textContent = sector.name;
                collaboratorSectorSelect.appendChild(option);
            });
        }
        
        console.log('✅ Selects de setores corrigidos!');
    },
    
    // Corrigir formulário de colaboradores
    fixCollaboratorForm: function() {
        console.log('🔧 Corrigindo formulário de colaboradores...');
        
        // Substituir Alpine.js por vanilla JS
        const collaboratorForm = document.getElementById('collaboratorForm');
        if (collaboratorForm) {
            // Corrigir inputs
            const nameInput = document.getElementById('collaboratorName');
            const emailInput = document.querySelector('input[x-model="newCollaborator.email"]');
            const positionInput = document.querySelector('input[x-model="newCollaborator.position"]');
            const sectorSelect = document.querySelector('select[x-model="newCollaborator.sectorId"]');
            const phoneInput = document.querySelector('input[x-model="newCollaborator.phone"]');
            const statusSelect = document.querySelector('select[x-model="newCollaborator.status"]');
            
            // Adicionar IDs se não existirem
            if (emailInput && !emailInput.id) emailInput.id = 'collaboratorEmail';
            if (positionInput && !positionInput.id) positionInput.id = 'collaboratorPosition';
            if (sectorSelect && !sectorSelect.id) sectorSelect.id = 'collaboratorSector';
            if (phoneInput && !phoneInput.id) phoneInput.id = 'collaboratorPhone';
            if (statusSelect && !statusSelect.id) statusSelect.id = 'collaboratorStatus';
            
            // Corrigir botão de adicionar colaborador
            const addButton = document.querySelector('button[x-text*="Cadastrar Colaborador"]');
            if (addButton) {
                addButton.onclick = function() {
                    window.metasApp.addCollaborator();
                };
            }
            
            // Corrigir botão de cancelar
            const cancelButton = document.querySelector('button[x-text="Cancelar"]');
            if (cancelButton) {
                cancelButton.onclick = function() {
                    window.metasApp.cancelCollaboratorEdit();
                };
            }
        }
        
        console.log('✅ Formulário de colaboradores corrigido!');
    },
    
    // Corrigir função de adicionar colaborador
    fixAddCollaborator: function() {
        console.log('🔧 Corrigindo função de adicionar colaborador...');
        
        // Sobrescrever função original
        window.metasApp.addCollaborator = function() {
            const name = document.getElementById('collaboratorName')?.value || '';
            const email = document.getElementById('collaboratorEmail')?.value || '';
            const sectorId = document.getElementById('collaboratorSector')?.value || '';
            const position = document.getElementById('collaboratorPosition')?.value || '';
            const phone = document.getElementById('collaboratorPhone')?.value || '';
            const status = document.getElementById('collaboratorStatus')?.value || 'ativo';
            
            if (!name || !email || !sectorId) {
                alert('Por favor, preencha os campos obrigatórios (Nome, E-mail e Setor)');
                return;
            }
            
            const collaborator = {
                id: this.editingCollaboratorId ? this.editingCollaboratorId : Date.now().toString(),
                name: name,
                email: email,
                sectorId: sectorId,
                position: position,
                phone: phone,
                status: status
            };
            
            if (this.editingCollaboratorId) {
                // Atualizar colaborador existente
                const index = this.collaborators.findIndex(c => c.id === this.editingCollaboratorId);
                if (index !== -1) {
                    this.collaborators[index] = collaborator;
                }
                this.editingCollaboratorId = null;
                alert('Colaborador atualizado com sucesso!');
            } else {
                // Adicionar novo colaborador
                this.collaborators.push(collaborator);
                alert('Colaborador adicionado com sucesso!');
            }
            
            // Limpar formulário
            document.getElementById('collaboratorName').value = '';
            document.getElementById('collaboratorEmail').value = '';
            document.getElementById('collaboratorSector').value = '';
            document.getElementById('collaboratorPosition').value = '';
            document.getElementById('collaboratorPhone').value = '';
            document.getElementById('collaboratorStatus').value = 'ativo';
            
            // Esconder formulário
            document.getElementById('collaboratorForm').style.display = 'none';
            
            // Salvar dados
            this.saveData();
            
            // Recarregar lista
            this.loadCollaboratorsList();
        };
        
        console.log('✅ Função de adicionar colaborador corrigida!');
    },
    
    // Corrigir função de cancelar edição de colaborador
    fixCancelCollaboratorEdit: function() {
        console.log('🔧 Corrigindo função de cancelar edição...');
        
        window.metasApp.cancelCollaboratorEdit = function() {
            this.editingCollaboratorId = null;
            
            // Limpar formulário
            document.getElementById('collaboratorName').value = '';
            document.getElementById('collaboratorEmail').value = '';
            document.getElementById('collaboratorSector').value = '';
            document.getElementById('collaboratorPosition').value = '';
            document.getElementById('collaboratorPhone').value = '';
            document.getElementById('collaboratorStatus').value = 'ativo';
            
            // Esconder formulário
            document.getElementById('collaboratorForm').style.display = 'none';
        };
        
        console.log('✅ Função de cancelar edição corrigida!');
    },
    
    // Aplicar todas as correções
    applyAllFixes: function() {
        console.log('🚀 Aplicando correções no sistema de metas...');
        
        this.fixSectorSelects();
        this.fixCollaboratorForm();
        this.fixAddCollaborator();
        this.fixCancelCollaboratorEdit();
        
        console.log('✅ Todas as correções aplicadas!');
        console.log('🎯 Sistema de metas agora deve funcionar corretamente!');
    }
};

// Aplicar correções quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    // Aguardar um pouco para o sistema original carregar
    setTimeout(function() {
        window.metasFix.applyAllFixes();
    }, 1000);
});

// Função global para aplicar correções manualmente
function fixMetasSystem() {
    window.metasFix.applyAllFixes();
} 