import json
import os
from typing import List, Dict, Optional
from datetime import datetime
import uuid
from app.modules.rh.models import Equipment, RHModels

class EquipmentRepository:
    """Repositório para gerenciar equipamentos"""
    
    def __init__(self):
        self.data_file = "app/data/equipment.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Garante que o arquivo de dados existe"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_data(self) -> List[Dict]:
        """Carrega dados do arquivo JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, data: List[Dict]):
        """Salva dados no arquivo JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all(self) -> List[Equipment]:
        """Retorna todos os equipamentos"""
        data = self._load_data()
        return [RHModels.dict_to_equipment(item) for item in data]
    
    def get_by_id(self, equipment_id: str) -> Optional[Equipment]:
        """Retorna um equipamento por ID"""
        data = self._load_data()
        for item in data:
            if item.get('id') == equipment_id:
                return RHModels.dict_to_equipment(item)
        return None
    
    def get_by_employee(self, employee_id: str) -> List[Equipment]:
        """Retorna equipamentos de um funcionário específico"""
        equipment_list = self.get_all()
        return [eq for eq in equipment_list if eq.assigned_to == employee_id]
    
    def get_active(self) -> List[Equipment]:
        """Retorna apenas equipamentos ativos"""
        equipment_list = self.get_all()
        return [eq for eq in equipment_list if eq.status == 'active']
    
    def create(self, equipment_data: Dict) -> Equipment:
        """Cria um novo equipamento"""
        equipment_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        equipment = Equipment(
            id=equipment_id,
            name=equipment_data['name'],
            type=equipment_data['type'],
            serial_number=equipment_data['serial_number'],
            brand=equipment_data['brand'],
            model=equipment_data['model'],
            assigned_to=equipment_data['assigned_to'],
            purchase_date=equipment_data['purchase_date'],
            warranty_expiry=equipment_data['warranty_expiry'],
            status=equipment_data.get('status', 'active'),
            created_at=now,
            updated_at=now,
            notes=equipment_data.get('notes'),
            photo_path=equipment_data.get('photo_path')
        )
        
        data = self._load_data()
        data.append(RHModels.equipment_to_dict(equipment))
        self._save_data(data)
        
        return equipment
    
    def update(self, equipment_id: str, equipment_data: Dict) -> Optional[Equipment]:
        """Atualiza um equipamento"""
        data = self._load_data()
        
        for i, item in enumerate(data):
            if item.get('id') == equipment_id:
                now = datetime.now().isoformat()
                
                # Atualiza apenas os campos fornecidos
                for key, value in equipment_data.items():
                    if key in ['name', 'type', 'serial_number', 'brand', 'model', 
                              'assigned_to', 'purchase_date', 'warranty_expiry', 
                              'status', 'notes', 'photo_path']:
                        item[key] = value
                
                item['updated_at'] = now
                
                self._save_data(data)
                return RHModels.dict_to_equipment(item)
        
        return None
    
    def delete(self, equipment_id: str) -> bool:
        """Remove um equipamento"""
        data = self._load_data()
        
        for i, item in enumerate(data):
            if item.get('id') == equipment_id:
                data.pop(i)
                self._save_data(data)
                return True
        
        return False
    
    def search(self, query: str) -> List[Equipment]:
        """Busca equipamentos por nome, marca, modelo ou número de série"""
        equipment_list = self.get_all()
        query = query.lower()
        
        results = []
        for equipment in equipment_list:
            if (query in equipment.name.lower() or 
                query in equipment.brand.lower() or 
                query in equipment.model.lower() or
                query in equipment.serial_number.lower()):
                results.append(equipment)
        
        return results
    
    def get_by_type(self, equipment_type: str) -> List[Equipment]:
        """Retorna equipamentos por tipo"""
        equipment_list = self.get_all()
        return [eq for eq in equipment_list if eq.type == equipment_type]
    
    def get_warranty_expiring_soon(self, days: int = 30) -> List[Equipment]:
        """Retorna equipamentos com garantia expirando em X dias"""
        from datetime import datetime, timedelta
        
        equipment_list = self.get_active()
        threshold_date = datetime.now() + timedelta(days=days)
        
        results = []
        for equipment in equipment_list:
            try:
                warranty_date = datetime.fromisoformat(equipment.warranty_expiry)
                if warranty_date <= threshold_date:
                    results.append(equipment)
            except ValueError:
                continue
        
        return results 