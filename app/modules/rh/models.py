"""
Sistema RH isolado: não adicionar código que afete outras funcionalidades.
Qualquer alteração deve ser aprovada.
"""

from datetime import datetime
import uuid
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
import json
import os

@dataclass
class Employee:
    """Modelo para funcionários"""
    id: str
    name: str
    position: str
    department: str
    email: str
    phone: str
    hire_date: str
    status: str  # 'active', 'inactive', 'on_leave'
    created_at: str
    updated_at: str
    notes: Optional[str] = None

@dataclass
class Equipment:
    """Modelo para equipamentos"""
    id: str
    name: str
    type: str  # 'notebook', 'desktop', 'monitor', 'peripheral', 'other'
    serial_number: str
    brand: str
    model: str
    assigned_to: str  # ID do funcionário
    purchase_date: str
    warranty_expiry: str
    status: str  # 'active', 'maintenance', 'retired', 'lost'
    created_at: str
    updated_at: str
    notes: Optional[str] = None
    photo_path: Optional[str] = None

@dataclass
class Document:
    """Modelo para documentos RH"""
    id: str
    title: str
    type: str  # 'contract', 'policy', 'procedure', 'form', 'other'
    category: str  # 'employment', 'equipment', 'policy', 'training', 'other'
    file_path: str
    created_at: str
    updated_at: str
    employee_id: Optional[str] = None
    equipment_id: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = None

@dataclass
class Contract:
    """Modelo para contratos"""
    id: str
    employee_id: str
    contract_type: str  # 'clt', 'pj', 'internship', 'temporary'
    start_date: str
    salary: float
    position: str
    status: str  # 'active', 'terminated', 'expired'
    created_at: str
    updated_at: str
    end_date: Optional[str] = None
    file_path: Optional[str] = None
    notes: Optional[str] = None

class RHModels:
    """Classe para gerenciar os modelos RH"""
    
    @staticmethod
    def employee_to_dict(employee: Employee) -> Dict[str, Any]:
        return asdict(employee)
    
    @staticmethod
    def dict_to_employee(data: Dict[str, Any]) -> Employee:
        return Employee(**data)
    
    @staticmethod
    def equipment_to_dict(equipment: Equipment) -> Dict[str, Any]:
        return asdict(equipment)
    
    @staticmethod
    def dict_to_equipment(data: Dict[str, Any]) -> Equipment:
        return Equipment(**data)
    
    @staticmethod
    def document_to_dict(document: Document) -> Dict[str, Any]:
        return asdict(document)
    
    @staticmethod
    def dict_to_document(data: Dict[str, Any]) -> Document:
        return Document(**data)
    
    @staticmethod
    def contract_to_dict(contract: Contract) -> Dict[str, Any]:
        return asdict(contract)
    
    @staticmethod
    def dict_to_contract(data: Dict[str, Any]) -> Contract:
        return Contract(**data) 



class CorporateDocument:
    """Modelo para documentos corporativos"""
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id', str(uuid.uuid4()))
        self.title = data.get('title', '')
        self.type = data.get('type', '')  # ata, documento, relatorio, etc.
        self.content = data.get('content', '')
        self.employee_id = data.get('employee_id', '')  # funcionário relacionado
        self.department = data.get('department', '')
        self.status = data.get('status', 'active')  # active, archived, draft
        self.tags = data.get('tags', [])
        self.attachments = data.get('attachments', [])
        self.created_by = data.get('created_by', '')
        self.created_at = data.get('created_at', datetime.now().isoformat())
        self.updated_at = data.get('updated_at', datetime.now().isoformat())
        self.published_at = data.get('published_at', '')

class DocumentAttachment:
    """Modelo para anexos de documentos"""
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id', str(uuid.uuid4()))
        self.document_id = data.get('document_id', '')
        self.filename = data.get('filename', '')
        self.original_filename = data.get('original_filename', '')
        self.file_path = data.get('file_path', '')
        self.file_size = data.get('file_size', 0)
        self.file_type = data.get('file_type', '')
        self.uploaded_by = data.get('uploaded_by', '')
        self.uploaded_at = data.get('uploaded_at', datetime.now().isoformat()) 