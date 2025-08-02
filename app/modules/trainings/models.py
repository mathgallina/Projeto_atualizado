"""
Modelos para o Sistema de Treinamentos Internos
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class Training:
    """Modelo para representar um treinamento"""
    id: str
    title: str
    description: str
    category: str
    duration: int  # em minutos
    difficulty: str  # 'beginner', 'intermediate', 'advanced'
    instructor: str
    materials: List[str]  # URLs dos materiais
    video_url: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    is_active: bool = True
    completion_rate: float = 0.0
    participants_count: int = 0


@dataclass
class TrainingProgress:
    """Modelo para acompanhar o progresso do usuário em um treinamento"""
    user_id: str
    training_id: str
    progress_percentage: float
    completed_modules: List[str]
    started_at: datetime
    completed_at: Optional[datetime] = None
    certificate_url: Optional[str] = None


@dataclass
class TrainingCategory:
    """Modelo para categorias de treinamento"""
    id: str
    name: str
    description: str
    icon: str
    color: str
    trainings_count: int = 0 