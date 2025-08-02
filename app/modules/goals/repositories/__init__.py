"""
Repositórios - Sistema de Metas
CDD v2.0 - Repositórios para acesso a dados de metas
"""

from .goals_repository import GoalsRepository
from .collaborators_repository import CollaboratorsRepository
from .sectors_repository import SectorsRepository

__all__ = [
    'GoalsRepository',
    'CollaboratorsRepository', 
    'SectorsRepository'
] 