from typing import List, Dict, Optional
from app.modules.rh.repositories.employee_repository import EmployeeRepository
from app.modules.rh.repositories.equipment_repository import EquipmentRepository
from app.modules.rh.models import Employee, Equipment

class RHService:
    """Serviço principal para gerenciar recursos humanos"""
    
    def __init__(self):
        self.employee_repo = EmployeeRepository()
        self.equipment_repo = EquipmentRepository()
    
    # Métodos para funcionários
    def get_all_employees(self) -> List[Employee]:
        """Retorna todos os funcionários"""
        return self.employee_repo.get_all()
    
    def get_active_employees(self) -> List[Employee]:
        """Retorna apenas funcionários ativos"""
        return self.employee_repo.get_active()
    
    def get_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        """Retorna um funcionário por ID"""
        return self.employee_repo.get_by_id(employee_id)
    
    def create_employee(self, employee_data: Dict) -> Employee:
        """Cria um novo funcionário"""
        return self.employee_repo.create(employee_data)
    
    def update_employee(self, employee_id: str, employee_data: Dict) -> Optional[Employee]:
        """Atualiza um funcionário"""
        return self.employee_repo.update(employee_id, employee_data)
    
    def delete_employee(self, employee_id: str) -> bool:
        """Remove um funcionário"""
        return self.employee_repo.delete(employee_id)
    
    def search_employees(self, query: str) -> List[Employee]:
        """Busca funcionários"""
        return self.employee_repo.search(query)
    
    # Métodos para equipamentos
    def get_all_equipment(self) -> List[Equipment]:
        """Retorna todos os equipamentos"""
        return self.equipment_repo.get_all()
    
    def get_active_equipment(self) -> List[Equipment]:
        """Retorna apenas equipamentos ativos"""
        return self.equipment_repo.get_active()
    
    def get_equipment_by_id(self, equipment_id: str) -> Optional[Equipment]:
        """Retorna um equipamento por ID"""
        return self.equipment_repo.get_by_id(equipment_id)
    
    def get_equipment_by_employee(self, employee_id: str) -> List[Equipment]:
        """Retorna equipamentos de um funcionário"""
        return self.equipment_repo.get_by_employee(employee_id)
    
    def create_equipment(self, equipment_data: Dict) -> Equipment:
        """Cria um novo equipamento"""
        return self.equipment_repo.create(equipment_data)
    
    def update_equipment(self, equipment_id: str, equipment_data: Dict) -> Optional[Equipment]:
        """Atualiza um equipamento"""
        return self.equipment_repo.update(equipment_id, equipment_data)
    
    def delete_equipment(self, equipment_id: str) -> bool:
        """Remove um equipamento"""
        return self.equipment_repo.delete(equipment_id)
    
    def search_equipment(self, query: str) -> List[Equipment]:
        """Busca equipamentos"""
        return self.equipment_repo.search(query)
    
    def get_equipment_by_type(self, equipment_type: str) -> List[Equipment]:
        """Retorna equipamentos por tipo"""
        return self.equipment_repo.get_by_type(equipment_type)
    
    def get_warranty_expiring_soon(self, days: int = 30) -> List[Equipment]:
        """Retorna equipamentos com garantia expirando em X dias"""
        return self.equipment_repo.get_warranty_expiring_soon(days)
    
    # Métodos combinados
    def get_employee_with_equipment(self, employee_id: str) -> Dict:
        """Retorna funcionário com seus equipamentos"""
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            return None
        
        equipment = self.get_equipment_by_employee(employee_id)
        
        return {
            'employee': employee,
            'equipment': equipment,
            'equipment_count': len(equipment)
        }
    
    def get_dashboard_stats(self) -> Dict:
        """Retorna estatísticas do dashboard RH"""
        employees = self.get_all_employees()
        equipment = self.get_all_equipment()
        
        active_employees = len([e for e in employees if e.status == 'active'])
        total_equipment = len(equipment)
        active_equipment = len([e for e in equipment if e.status == 'active'])
        
        # Equipamentos por tipo
        equipment_by_type = {}
        for eq in equipment:
            if eq.type not in equipment_by_type:
                equipment_by_type[eq.type] = 0
            equipment_by_type[eq.type] += 1
        
        # Funcionários por departamento
        employees_by_dept = {}
        for emp in employees:
            if emp.department not in employees_by_dept:
                employees_by_dept[emp.department] = 0
            employees_by_dept[emp.department] += 1
        
        return {
            'total_employees': len(employees),
            'active_employees': active_employees,
            'total_equipment': total_equipment,
            'active_equipment': active_equipment,
            'equipment_by_type': equipment_by_type,
            'employees_by_department': employees_by_dept,
            'warranty_expiring_soon': len(self.get_warranty_expiring_soon(30))
        } 