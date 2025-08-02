"""
Repositório para gerenciamento de dados dos treinamentos
"""

import json
import os
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class TrainingRepository:
    """Repositório para gerenciar dados dos treinamentos"""
    
    def __init__(self, db_manager=None):
        """Inicializa o repositório"""
        self.data_file = "app/data/trainings.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Garante que o arquivo de dados existe"""
        if not os.path.exists(self.data_file):
            # Criar estrutura básica se o arquivo não existir
            default_data = {
                "categories": [],
                "trainings": [],
                "progress": []
            }
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)
    
    def _load_data(self) -> Dict[str, Any]:
        """Carrega os dados do arquivo JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar dados de treinamentos: {e}")
            return {"categories": [], "trainings": [], "progress": []}
    
    def _save_data(self, data: Dict[str, Any]):
        """Salva os dados no arquivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar dados de treinamentos: {e}")
    
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """Retorna todas as categorias de treinamento"""
        data = self._load_data()
        return data.get("categories", [])
    
    def get_category_by_id(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Retorna uma categoria específica por ID"""
        categories = self.get_all_categories()
        for category in categories:
            if category.get("id") == category_id:
                return category
        return None
    
    def get_all_trainings(self) -> List[Dict[str, Any]]:
        """Retorna todos os treinamentos"""
        data = self._load_data()
        return data.get("trainings", [])
    
    def get_training_by_id(self, training_id: str) -> Optional[Dict[str, Any]]:
        """Retorna um treinamento específico por ID"""
        trainings = self.get_all_trainings()
        for training in trainings:
            if training.get("id") == training_id:
                return training
        return None
    
    def get_trainings_by_category(self, category_id: str) -> List[Dict[str, Any]]:
        """Retorna treinamentos de uma categoria específica"""
        trainings = self.get_all_trainings()
        return [t for t in trainings if t.get("category") == category_id]
    
    def get_recent_trainings(self, limit: int = 4) -> List[Dict[str, Any]]:
        """Retorna os treinamentos mais recentes"""
        trainings = self.get_all_trainings()
        # Ordenar por data de criação (mais recente primeiro)
        sorted_trainings = sorted(
            trainings, 
            key=lambda x: x.get("created_at", ""), 
            reverse=True
        )
        return sorted_trainings[:limit]
    
    def get_user_progress(self, user_id: str) -> List[Dict[str, Any]]:
        """Retorna o progresso de um usuário específico"""
        data = self._load_data()
        progress = data.get("progress", [])
        return [p for p in progress if p.get("user_id") == user_id]
    
    def get_training_progress(self, user_id: str, training_id: str) -> Optional[Dict[str, Any]]:
        """Retorna o progresso de um usuário em um treinamento específico"""
        progress_list = self.get_user_progress(user_id)
        for progress in progress_list:
            if progress.get("training_id") == training_id:
                return progress
        return None
    
    def update_progress(self, user_id: str, training_id: str, progress_data: Dict[str, Any]):
        """Atualiza o progresso de um usuário em um treinamento"""
        data = self._load_data()
        progress_list = data.get("progress", [])
        
        # Procurar progresso existente
        existing_progress = None
        for i, progress in enumerate(progress_list):
            if progress.get("user_id") == user_id and progress.get("training_id") == training_id:
                existing_progress = i
                break
        
        # Criar novo progresso ou atualizar existente
        new_progress = {
            "user_id": user_id,
            "training_id": training_id,
            "progress_percentage": progress_data.get("progress_percentage", 0),
            "completed_modules": progress_data.get("completed_modules", []),
            "started_at": progress_data.get("started_at", datetime.now().isoformat()),
            "completed_at": progress_data.get("completed_at"),
            "certificate_url": progress_data.get("certificate_url")
        }
        
        if existing_progress is not None:
            progress_list[existing_progress] = new_progress
        else:
            progress_list.append(new_progress)
        
        data["progress"] = progress_list
        self._save_data(data)
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais dos treinamentos"""
        data = self._load_data()
        trainings = self.get_all_trainings()
        categories = self.get_all_categories()
        progress_list = data.get("progress", [])
        
        total_trainings = len(trainings)
        total_categories = len(categories)
        
        # Calcular taxa média de conclusão baseada no progresso real dos usuários
        if progress_list:
            # Filtrar apenas progressos com 100% de conclusão
            completed_progress = [p for p in progress_list if p.get("progress_percentage", 0) == 100]
            total_progress = len(progress_list)
            
            if total_progress > 0:
                avg_completion_rate = (len(completed_progress) / total_progress) * 100
            else:
                avg_completion_rate = 0
        else:
            avg_completion_rate = 0
        
        # Contar participantes únicos
        unique_participants = len(set(p.get("user_id") for p in progress_list))
        
        return {
            "total_trainings": total_trainings,
            "total_categories": total_categories,
            "avg_completion_rate": round(avg_completion_rate, 1),
            "total_participants": unique_participants
        }
    
    def create_training(self, training_data: Dict[str, Any]) -> str:
        """Cria um novo treinamento"""
        try:
            data = self._load_data()
            trainings = data.get("trainings", [])
            
            # Gerar ID único
            import uuid
            training_id = str(uuid.uuid4())
            
            # Criar treinamento
            new_training = {
                "id": training_id,
                "title": training_data.get("title"),
                "description": training_data.get("description"),
                "category": training_data.get("category"),
                "duration": training_data.get("duration", 0),
                "difficulty": training_data.get("difficulty", "beginner"),
                "instructor": training_data.get("instructor"),
                "materials": training_data.get("materials", []),
                "video_url": training_data.get("video_url"),
                "completion_rate": 0.0,
                "participants_count": 0,
                "is_active": training_data.get("is_active", True),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            trainings.append(new_training)
            data["trainings"] = trainings
            
            self._save_data(data)
            logger.info(f"Treinamento criado com ID: {training_id}")
            return training_id
            
        except Exception as e:
            logger.error(f"Erro ao criar treinamento: {e}")
            raise
    
    def update_training(self, training_id: str, training_data: Dict[str, Any]) -> bool:
        """Atualiza um treinamento existente"""
        try:
            data = self._load_data()
            trainings = data.get("trainings", [])
            
            # Encontrar e atualizar o treinamento
            for i, training in enumerate(trainings):
                if training.get("id") == training_id:
                    trainings[i].update({
                        "title": training_data.get("title"),
                        "description": training_data.get("description"),
                        "category": training_data.get("category"),
                        "duration": training_data.get("duration", 0),
                        "difficulty": training_data.get("difficulty", "beginner"),
                        "instructor": training_data.get("instructor"),
                        "materials": training_data.get("materials", []),
                        "video_url": training_data.get("video_url"),
                        "is_active": training_data.get("is_active", True),
                        "updated_at": datetime.now().isoformat()
                    })
                    
                    self._save_data(data)
                    logger.info(f"Treinamento atualizado: {training_id}")
                    return True
            
            logger.error(f"Treinamento não encontrado: {training_id}")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao atualizar treinamento: {e}")
            raise
    
    def delete_training(self, training_id: str) -> bool:
        """Exclui um treinamento"""
        try:
            data = self._load_data()
            trainings = data.get("trainings", [])
            
            # Encontrar e remover o treinamento
            for i, training in enumerate(trainings):
                if training.get("id") == training_id:
                    # Remover materiais associados
                    materials = training.get("materials", [])
                    for material in materials:
                        file_path = os.path.join(self.data_file.rsplit('/', 1)[0].replace('data', 'static/uploads/trainings'), material)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    
                    # Remover treinamento
                    trainings.pop(i)
                    self._save_data(data)
                    logger.info(f"Treinamento excluído: {training_id}")
                    return True
            
            logger.error(f"Treinamento não encontrado: {training_id}")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao excluir treinamento: {e}")
            raise 