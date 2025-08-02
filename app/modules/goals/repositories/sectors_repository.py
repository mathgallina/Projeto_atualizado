"""
Repositório de Setores - Sistema de Metas
CDD v2.0 - Acesso a dados de setores
"""

import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4

from app.core.database import DatabaseManager
from ..models import Sector


class SectorsRepository:
    """Repositório para gerenciar dados de setores"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.data_file = os.path.join(db_manager.data_folder, "sectors.json")
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
    
    def get_all_sectors(self) -> List[Sector]:
        """Retorna todos os setores"""
        data = self._load_data()
        sectors = []
        for sector_data in data:
            try:
                sector = Sector.from_dict(sector_data)
                sectors.append(sector)
            except Exception as e:
                print(f"Erro ao carregar setor {sector_data.get('id', 'unknown')}: {e}")
        return sectors
    
    def get_sector_by_id(self, sector_id: str) -> Optional[Sector]:
        """Retorna um setor específico por ID"""
        sectors = self.get_all_sectors()
        for sector in sectors:
            if sector.id == sector_id:
                return sector
        return None
    
    def create_sector(self, sector_data: Dict[str, Any]) -> Sector:
        """Cria um novo setor"""
        sectors = self.get_all_sectors()
        
        # Gera ID único se não fornecido
        if 'id' not in sector_data:
            sector_data['id'] = str(uuid4())
        
        sector_data['created_at'] = datetime.now()
        
        # Cria instância do setor
        sector = Sector.from_dict(sector_data)
        
        # Adiciona à lista
        sectors.append(sector)
        
        # Salva dados
        data = [s.to_dict() for s in sectors]
        self._save_data(data)
        
        return sector
    
    def update_sector(self, sector_id: str, sector_data: Dict[str, Any]) -> Optional[Sector]:
        """Atualiza um setor existente"""
        sectors = self.get_all_sectors()
        
        for i, sector in enumerate(sectors):
            if sector.id == sector_id:
                # Atualiza campos
                for key, value in sector_data.items():
                    if hasattr(sector, key):
                        setattr(sector, key, value)
                
                # Salva dados
                data = [s.to_dict() for s in sectors]
                self._save_data(data)
                
                return sector
        
        return None
    
    def delete_sector(self, sector_id: str) -> bool:
        """Deleta um setor"""
        sectors = self.get_all_sectors()
        
        for i, sector in enumerate(sectors):
            if sector.id == sector_id:
                sectors.pop(i)
                
                # Salva dados
                data = [s.to_dict() for s in sectors]
                self._save_data(data)
                
                return True
        
        return False
    
    def search_sectors(self, search_term: str) -> List[Sector]:
        """Busca setores por nome"""
        sectors = self.get_all_sectors()
        search_term = search_term.lower()
        
        return [
            s for s in sectors 
            if search_term in s.name.lower() or 
               search_term in s.description.lower()
        ]
    
    def initialize_default_sectors(self):
        """Inicializa setores padrão se não existirem"""
        sectors = self.get_all_sectors()
        
        if not sectors:
            default_sectors = [
                {
                    "id": "comercial",
                    "name": "Comercial",
                    "description": "Setor responsável por vendas e relacionamento com clientes",
                    "color": "blue",
                    "icon": "fas fa-handshake"
                },
                {
                    "id": "tecnico",
                    "name": "Técnico",
                    "description": "Setor responsável por instalação e manutenção técnica",
                    "color": "green",
                    "icon": "fas fa-tools"
                },
                {
                    "id": "financeiro",
                    "name": "Financeiro",
                    "description": "Setor responsável por contabilidade e finanças",
                    "color": "yellow",
                    "icon": "fas fa-calculator"
                },
                {
                    "id": "rh",
                    "name": "Recursos Humanos",
                    "description": "Setor responsável por gestão de pessoas",
                    "color": "purple",
                    "icon": "fas fa-users"
                },
                {
                    "id": "ti",
                    "name": "Tecnologia da Informação",
                    "description": "Setor responsável por sistemas e tecnologia",
                    "color": "indigo",
                    "icon": "fas fa-laptop-code"
                },
                {
                    "id": "marketing",
                    "name": "Marketing",
                    "description": "Setor responsável por marketing e comunicação",
                    "color": "pink",
                    "icon": "fas fa-bullhorn"
                }
            ]
            
            for sector_data in default_sectors:
                self.create_sector(sector_data) 