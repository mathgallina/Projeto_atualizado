"""
Repositório de Colaboradores - Sistema de Metas
CDD v2.0 - Acesso a dados de colaboradores
"""

import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4

from app.core.database import DatabaseManager
from ..models import Collaborator


class CollaboratorsRepository:
    """Repositório para gerenciar dados de colaboradores"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.data_file = os.path.join(db_manager.data_folder, "collaborators.json")
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Garante que o arquivo de dados existe"""
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Carrega dados do arquivo JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, data: List[Dict[str, Any]]):
        """Salva dados no arquivo JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all_collaborators(self) -> List[Collaborator]:
        """Retorna todos os colaboradores"""
        data = self._load_data()
        collaborators = []
        for collab_data in data:
            try:
                collaborator = Collaborator.from_dict(collab_data)
                collaborators.append(collaborator)
            except Exception as e:
                print(f"Erro ao carregar colaborador {collab_data.get('id', 'unknown')}: {e}")
        return collaborators
    
    def get_collaborator_by_id(self, collaborator_id: str) -> Optional[Collaborator]:
        """Retorna um colaborador específico por ID"""
        collaborators = self.get_all_collaborators()
        for collaborator in collaborators:
            if collaborator.id == collaborator_id:
                return collaborator
        return None
    
    def get_collaborators_by_sector(self, sector_id: str) -> List[Collaborator]:
        """Retorna colaboradores de um setor específico"""
        collaborators = self.get_all_collaborators()
        return [c for c in collaborators if c.sector_id == sector_id]
    
    def create_collaborator(self, collaborator_data: Dict[str, Any]) -> Collaborator:
        """Cria um novo colaborador"""
        collaborators = self.get_all_collaborators()
        
        # Gera ID único
        collaborator_data['id'] = str(uuid4())
        collaborator_data['created_at'] = datetime.now()
        
        # Cria instância do colaborador
        collaborator = Collaborator.from_dict(collaborator_data)
        
        # Adiciona à lista
        collaborators.append(collaborator)
        
        # Salva dados
        data = [c.to_dict() for c in collaborators]
        self._save_data(data)
        
        return collaborator
    
    def update_collaborator(self, collaborator_id: str, collaborator_data: Dict[str, Any]) -> Optional[Collaborator]:
        """Atualiza um colaborador existente"""
        collaborators = self.get_all_collaborators()
        
        for i, collaborator in enumerate(collaborators):
            if collaborator.id == collaborator_id:
                # Atualiza campos
                for key, value in collaborator_data.items():
                    if hasattr(collaborator, key):
                        setattr(collaborator, key, value)
                
                # Salva dados
                data = [c.to_dict() for c in collaborators]
                self._save_data(data)
                
                return collaborator
        
        return None
    
    def delete_collaborator(self, collaborator_id: str) -> bool:
        """Deleta um colaborador"""
        collaborators = self.get_all_collaborators()
        
        for i, collaborator in enumerate(collaborators):
            if collaborator.id == collaborator_id:
                collaborators.pop(i)
                
                # Salva dados
                data = [c.to_dict() for c in collaborators]
                self._save_data(data)
                
                return True
        
        return False
    
    def search_collaborators(self, search_term: str) -> List[Collaborator]:
        """Busca colaboradores por nome"""
        collaborators = self.get_all_collaborators()
        search_term = search_term.lower()
        
        return [
            c for c in collaborators 
            if search_term in c.name.lower() or 
               (c.email and search_term in c.email.lower())
        ] 