"""
Repositório de Metas - Sistema de Metas
CDD v2.0 - Acesso a dados de metas
"""

import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4

from app.core.database import DatabaseManager
from ..models import Goal, GoalStatus


class GoalsRepository:
    """Repositório para gerenciar dados de metas"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.data_file = os.path.join(db_manager.data_folder, "goals.json")
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
    
    def get_all_goals(self) -> List[Goal]:
        """Retorna todas as metas"""
        data = self._load_data()
        goals = []
        for goal_data in data:
            try:
                goal = Goal.from_dict(goal_data)
                goal.update_status()  # Atualiza status baseado na data
                goals.append(goal)
            except Exception as e:
                print(f"Erro ao carregar meta {goal_data.get('id', 'unknown')}: {e}")
        return goals
    
    def get_goal_by_id(self, goal_id: str) -> Optional[Goal]:
        """Retorna uma meta específica por ID"""
        goals = self.get_all_goals()
        for goal in goals:
            if goal.id == goal_id:
                return goal
        return None
    
    def get_goals_by_collaborator(self, collaborator_id: str) -> List[Goal]:
        """Retorna metas de um colaborador específico"""
        goals = self.get_all_goals()
        return [goal for goal in goals if goal.collaborator_id == collaborator_id]
    
    def get_goals_by_sector(self, sector_id: str) -> List[Goal]:
        """Retorna metas de um setor específico"""
        goals = self.get_all_goals()
        return [goal for goal in goals if goal.sector_id == sector_id]
    
    def get_goals_by_status(self, status: GoalStatus) -> List[Goal]:
        """Retorna metas por status"""
        goals = self.get_all_goals()
        return [goal for goal in goals if goal.status == status]
    
    def create_goal(self, goal_data: Dict[str, Any]) -> Goal:
        """Cria uma nova meta"""
        goals = self.get_all_goals()
        
        # Gera ID único
        goal_data['id'] = str(uuid4())
        goal_data['created_at'] = datetime.now()
        goal_data['updated_at'] = datetime.now()
        
        # Cria instância da meta
        goal = Goal.from_dict(goal_data)
        
        # Adiciona à lista
        goals.append(goal)
        
        # Salva dados
        data = [g.to_dict() for g in goals]
        self._save_data(data)
        
        return goal
    
    def update_goal(self, goal_id: str, goal_data: Dict[str, Any]) -> Optional[Goal]:
        """Atualiza uma meta existente"""
        goals = self.get_all_goals()
        
        for i, goal in enumerate(goals):
            if goal.id == goal_id:
                # Atualiza campos
                for key, value in goal_data.items():
                    if hasattr(goal, key):
                        setattr(goal, key, value)
                
                goal.updated_at = datetime.now()
                goal.update_status()
                
                # Salva dados
                data = [g.to_dict() for g in goals]
                self._save_data(data)
                
                return goal
        
        return None
    
    def delete_goal(self, goal_id: str) -> bool:
        """Deleta uma meta"""
        goals = self.get_all_goals()
        
        for i, goal in enumerate(goals):
            if goal.id == goal_id:
                goals.pop(i)
                
                # Salva dados
                data = [g.to_dict() for g in goals]
                self._save_data(data)
                
                return True
        
        return False
    
    def get_goals_statistics(self) -> Dict[str, int]:
        """Retorna estatísticas das metas"""
        goals = self.get_all_goals()
        
        total = len(goals)
        completed = len([g for g in goals if g.status == GoalStatus.COMPLETED])
        overdue = len([g for g in goals if g.status == GoalStatus.OVERDUE])
        active = len([g for g in goals if g.status == GoalStatus.ACTIVE])
        
        return {
            'total': total,
            'completed': completed,
            'overdue': overdue,
            'active': active
        } 