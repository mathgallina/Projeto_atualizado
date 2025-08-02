import json
import os
from typing import List, Dict, Optional
from datetime import datetime
import uuid
from app.modules.rh.models import Employee, RHModels

class EmployeeRepository:
    """Repositório para gerenciar funcionários"""
    
    def __init__(self):
        self.data_file = "app/data/employees.json"
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
    
    def get_all(self) -> List[Employee]:
        """Retorna todos os funcionários"""
        data = self._load_data()
        return [RHModels.dict_to_employee(item) for item in data]
    
    def get_by_id(self, employee_id: str) -> Optional[Employee]:
        """Retorna um funcionário por ID"""
        data = self._load_data()
        for item in data:
            if item.get('id') == employee_id:
                return RHModels.dict_to_employee(item)
        return None
    
    def get_active(self) -> List[Employee]:
        """Retorna apenas funcionários ativos"""
        employees = self.get_all()
        return [emp for emp in employees if emp.status == 'active']
    
    def create(self, employee_data: Dict) -> Employee:
        """Cria um novo funcionário"""
        employee_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        employee = Employee(
            id=employee_id,
            name=employee_data['name'],
            position=employee_data['position'],
            department=employee_data['department'],
            email=employee_data['email'],
            phone=employee_data['phone'],
            hire_date=employee_data['hire_date'],
            status=employee_data.get('status', 'active'),
            created_at=now,
            updated_at=now,
            notes=employee_data.get('notes')
        )
        
        data = self._load_data()
        data.append(RHModels.employee_to_dict(employee))
        self._save_data(data)
        
        return employee
    
    def update(self, employee_id: str, employee_data: Dict) -> Optional[Employee]:
        """Atualiza um funcionário"""
        data = self._load_data()
        
        for i, item in enumerate(data):
            if item.get('id') == employee_id:
                now = datetime.now().isoformat()
                
                # Atualiza apenas os campos fornecidos
                for key, value in employee_data.items():
                    if key in ['name', 'position', 'department', 'email', 'phone', 'hire_date', 'status', 'notes']:
                        item[key] = value
                
                item['updated_at'] = now
                
                self._save_data(data)
                return RHModels.dict_to_employee(item)
        
        return None
    
    def delete(self, employee_id: str) -> bool:
        """Remove um funcionário"""
        data = self._load_data()
        
        for i, item in enumerate(data):
            if item.get('id') == employee_id:
                data.pop(i)
                self._save_data(data)
                return True
        
        return False
    
    def search(self, query: str) -> List[Employee]:
        """Busca funcionários por nome, email ou cargo"""
        employees = self.get_all()
        query = query.lower()
        
        results = []
        for employee in employees:
            if (query in employee.name.lower() or 
                query in employee.email.lower() or 
                query in employee.position.lower()):
                results.append(employee)
        
        return results 