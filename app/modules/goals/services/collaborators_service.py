"""
Serviço de Colaboradores - Sistema de Metas
CDD v2.0 - Lógica de negócio para colaboradores
"""

from typing import List, Optional, Dict, Any

from app.core.database import DatabaseManager
from ..repositories.collaborators_repository import CollaboratorsRepository
from ..repositories.sectors_repository import SectorsRepository
from ..models import Collaborator


class CollaboratorsService:
    """Serviço para gerenciar lógica de negócio dos colaboradores"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.collaborators_repo = CollaboratorsRepository(db_manager)
        self.sectors_repo = SectorsRepository(db_manager)
    
    def get_all_collaborators(self) -> List[Dict[str, Any]]:
        """Retorna todos os colaboradores com dados completos"""
        collaborators = self.collaborators_repo.get_all_collaborators()
        return [self._enrich_collaborator_data(collaborator) for collaborator in collaborators]
    
    def get_collaborator_by_id(self, collaborator_id: str) -> Optional[Dict[str, Any]]:
        """Retorna um colaborador específico com dados completos"""
        collaborator = self.collaborators_repo.get_collaborator_by_id(collaborator_id)
        if collaborator:
            return self._enrich_collaborator_data(collaborator)
        return None
    
    def get_collaborators_by_sector(self, sector_id: str) -> List[Dict[str, Any]]:
        """Retorna colaboradores de um setor específico"""
        collaborators = self.collaborators_repo.get_collaborators_by_sector(sector_id)
        return [self._enrich_collaborator_data(collaborator) for collaborator in collaborators]
    
    def create_collaborator(self, collaborator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo colaborador"""
        # Validações básicas
        if not collaborator_data.get('name'):
            raise ValueError("Nome do colaborador é obrigatório")
        
        if not collaborator_data.get('sector_id'):
            raise ValueError("Setor é obrigatório")
        
        # Verifica se setor existe
        sector = self.sectors_repo.get_sector_by_id(collaborator_data['sector_id'])
        if not sector:
            raise ValueError("Setor não encontrado")
        
        # Cria o colaborador
        collaborator = self.collaborators_repo.create_collaborator(collaborator_data)
        return self._enrich_collaborator_data(collaborator)
    
    def update_collaborator(self, collaborator_id: str, collaborator_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Atualiza um colaborador existente"""
        # Validações básicas
        if 'sector_id' in collaborator_data:
            sector = self.sectors_repo.get_sector_by_id(collaborator_data['sector_id'])
            if not sector:
                raise ValueError("Setor não encontrado")
        
        # Atualiza o colaborador
        collaborator = self.collaborators_repo.update_collaborator(collaborator_id, collaborator_data)
        if collaborator:
            return self._enrich_collaborator_data(collaborator)
        return None
    
    def delete_collaborator(self, collaborator_id: str) -> bool:
        """Deleta um colaborador"""
        return self.collaborators_repo.delete_collaborator(collaborator_id)
    
    def search_collaborators(self, search_term: str) -> List[Dict[str, Any]]:
        """Busca colaboradores por termo"""
        collaborators = self.collaborators_repo.search_collaborators(search_term)
        return [self._enrich_collaborator_data(collaborator) for collaborator in collaborators]
    
    def get_collaborators_for_select(self) -> List[Dict[str, Any]]:
        """Retorna colaboradores formatados para select"""
        collaborators = self.get_all_collaborators()
        return [
            {
                'id': collab['id'],
                'name': collab['name'],
                'sector_name': collab.get('sector', {}).get('name', 'N/A'),
                'text': f"{collab['name']} ({collab.get('sector', {}).get('name', 'N/A')})"
            }
            for collab in collaborators
        ]
    
    def _enrich_collaborator_data(self, collaborator: Collaborator) -> Dict[str, Any]:
        """Enriquece os dados do colaborador com informações do setor"""
        collaborator_data = collaborator.to_dict()
        
        # Adiciona dados do setor
        sector = self.sectors_repo.get_sector_by_id(collaborator.sector_id)
        if sector:
            collaborator_data['sector'] = sector.to_dict()
        
        return collaborator_data 