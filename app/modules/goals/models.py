"""
Modelos de Dados - Sistema de Metas
CDD v2.0 - Modelos para colaboradores, setores e metas

Este módulo define os modelos de dados para o sistema de metas,
incluindo validações e estruturas de dados.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class GoalStatus(str, Enum):
    """Status possíveis para uma meta"""
    ACTIVE = "ativo"
    COMPLETED = "concluido"
    OVERDUE = "atrasado"


@dataclass
class Sector:
    """Modelo para setor da empresa"""
    id: str
    name: str
    description: str
    color: str
    icon: str
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sector':
        """Cria instância a partir de dicionário"""
        if isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)


@dataclass
class Collaborator:
    """Modelo para colaborador"""
    id: str
    name: str
    sector_id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Collaborator':
        """Cria instância a partir de dicionário"""
        if data.get('created_at') and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)


@dataclass
class Goal:
    """Modelo para meta"""
    id: str
    title: str
    collaborator_id: str
    sector_id: str
    due_date: datetime
    description: Optional[str] = None
    status: GoalStatus = GoalStatus.ACTIVE
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['status'] = self.status.value
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            data['updated_at'] = self.updated_at.isoformat()
        data['due_date'] = self.due_date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Goal':
        """Cria instância a partir de dicionário"""
        if data.get('created_at') and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if data.get('updated_at') and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        if isinstance(data['due_date'], str):
            data['due_date'] = datetime.fromisoformat(data['due_date'])
        data['status'] = GoalStatus(data['status'])
        return cls(**data)
    
    def is_overdue(self) -> bool:
        """Verifica se a meta está atrasada"""
        return datetime.now() > self.due_date and self.status == GoalStatus.ACTIVE
    
    def update_status(self):
        """Atualiza o status da meta baseado na data de vencimento"""
        if self.status == GoalStatus.ACTIVE and self.is_overdue():
            self.status = GoalStatus.OVERDUE 