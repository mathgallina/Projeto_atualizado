"""
Serviço de Setores - Sistema de Metas
CDD v2.0 - Lógica de negócio para setores
"""

from typing import List, Optional, Dict, Any

from app.core.database import DatabaseManager
from ..repositories.sectors_repository import SectorsRepository
from ..models import Sector


class SectorsService:
    """Serviço para gerenciar lógica de negócio dos setores"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sectors_repo = SectorsRepository(db_manager)
        # Inicializa setores padrão se necessário
        self.sectors_repo.initialize_default_sectors()
    
    def get_all_sectors(self) -> List[Dict[str, Any]]:
        """Retorna todos os setores"""
        sectors = self.sectors_repo.get_all_sectors()
        return [sector.to_dict() for sector in sectors]
    
    def get_sector_by_id(self, sector_id: str) -> Optional[Dict[str, Any]]:
        """Retorna um setor específico"""
        sector = self.sectors_repo.get_sector_by_id(sector_id)
        if sector:
            return sector.to_dict()
        return None
    
    def create_sector(self, sector_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo setor"""
        # Validações básicas
        if not sector_data.get('name'):
            raise ValueError("Nome do setor é obrigatório")
        
        if not sector_data.get('description'):
            raise ValueError("Descrição do setor é obrigatória")
        
        # Valores padrão para campos opcionais
        if 'color' not in sector_data:
            sector_data['color'] = 'gray'
        
        if 'icon' not in sector_data:
            sector_data['icon'] = 'fas fa-building'
        
        # Cria o setor
        sector = self.sectors_repo.create_sector(sector_data)
        return sector.to_dict()
    
    def update_sector(self, sector_id: str, sector_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Atualiza um setor existente"""
        # Atualiza o setor
        sector = self.sectors_repo.update_sector(sector_id, sector_data)
        if sector:
            return sector.to_dict()
        return None
    
    def delete_sector(self, sector_id: str) -> bool:
        """Deleta um setor"""
        return self.sectors_repo.delete_sector(sector_id)
    
    def search_sectors(self, search_term: str) -> List[Dict[str, Any]]:
        """Busca setores por termo"""
        sectors = self.sectors_repo.search_sectors(search_term)
        return [sector.to_dict() for sector in sectors]
    
    def get_sectors_for_select(self) -> List[Dict[str, Any]]:
        """Retorna setores formatados para select"""
        sectors = self.get_all_sectors()
        return [
            {
                'id': sector['id'],
                'name': sector['name'],
                'text': sector['name']
            }
            for sector in sectors
        ]
    
    def get_sectors_with_stats(self) -> List[Dict[str, Any]]:
        """Retorna setores com estatísticas básicas"""
        sectors = self.get_all_sectors()
        
        # Aqui você pode adicionar lógica para calcular estatísticas por setor
        # Por exemplo, número de colaboradores, metas, etc.
        
        return sectors 