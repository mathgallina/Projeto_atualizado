import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.modules.rh.models import CorporateDocument, DocumentAttachment
import uuid

class DocumentRepository:
    """Repositório para gerenciar documentos corporativos"""
    
    def __init__(self):
        self.data_file = 'app/data/corporate_documents.json'
        self.attachments_dir = 'app/static/uploads/documents'
        self._ensure_data_file()
        self._ensure_attachments_dir()
    
    def _ensure_data_file(self):
        """Garante que o arquivo de dados existe"""
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _ensure_attachments_dir(self):
        """Garante que o diretório de anexos existe"""
        os.makedirs(self.attachments_dir, exist_ok=True)
    
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
    
    def get_all(self) -> List[CorporateDocument]:
        """Retorna todos os documentos"""
        data = self._load_data()
        return [CorporateDocument(doc) for doc in data]
    
    def get_by_id(self, document_id: str) -> Optional[CorporateDocument]:
        """Retorna um documento por ID"""
        data = self._load_data()
        for doc in data:
            if doc.get('id') == document_id:
                return CorporateDocument(doc)
        return None
    
    def get_by_employee(self, employee_id: str) -> List[CorporateDocument]:
        """Retorna documentos de um funcionário específico"""
        data = self._load_data()
        documents = []
        for doc in data:
            if doc.get('employee_id') == employee_id:
                documents.append(CorporateDocument(doc))
        return documents
    
    def get_by_type(self, doc_type: str) -> List[CorporateDocument]:
        """Retorna documentos por tipo"""
        data = self._load_data()
        documents = []
        for doc in data:
            if doc.get('type') == doc_type:
                documents.append(CorporateDocument(doc))
        return documents
    
    def get_by_department(self, department: str) -> List[CorporateDocument]:
        """Retorna documentos por departamento"""
        data = self._load_data()
        documents = []
        for doc in data:
            if doc.get('department') == department:
                documents.append(CorporateDocument(doc))
        return documents
    
    def search(self, query: str) -> List[CorporateDocument]:
        """Busca documentos por texto"""
        data = self._load_data()
        documents = []
        query_lower = query.lower()
        
        for doc in data:
            title = doc.get('title', '').lower()
            content = doc.get('content', '').lower()
            tags = [tag.lower() for tag in doc.get('tags', [])]
            
            if (query_lower in title or 
                query_lower in content or 
                any(query_lower in tag for tag in tags)):
                documents.append(CorporateDocument(doc))
        
        return documents
    
    def create(self, document_data: Dict[str, Any]) -> CorporateDocument:
        """Cria um novo documento"""
        data = self._load_data()
        
        document_data['id'] = document_data.get('id', str(uuid.uuid4()))
        document_data['created_at'] = datetime.now().isoformat()
        document_data['updated_at'] = datetime.now().isoformat()
        
        document = CorporateDocument(document_data)
        data.append(document_data)
        self._save_data(data)
        
        return document
    
    def update(self, document_id: str, document_data: Dict[str, Any]) -> Optional[CorporateDocument]:
        """Atualiza um documento"""
        data = self._load_data()
        
        for i, doc in enumerate(data):
            if doc.get('id') == document_id:
                document_data['id'] = document_id
                document_data['updated_at'] = datetime.now().isoformat()
                document_data['created_at'] = doc.get('created_at', datetime.now().isoformat())
                
                data[i] = document_data
                self._save_data(data)
                
                return CorporateDocument(document_data)
        
        return None
    
    def delete(self, document_id: str) -> bool:
        """Remove um documento"""
        data = self._load_data()
        
        for i, doc in enumerate(data):
            if doc.get('id') == document_id:
                # Remove anexos físicos
                self._delete_attachments(document_id)
                
                # Remove do JSON
                data.pop(i)
                self._save_data(data)
                return True
        
        return False
    
    def _delete_attachments(self, document_id: str):
        """Remove anexos físicos de um documento"""
        data = self._load_data()
        for doc in data:
            if doc.get('id') == document_id:
                attachments = doc.get('attachments', [])
                for attachment in attachments:
                    file_path = attachment.get('file_path')
                    if file_path and os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass
                break
    
    def add_attachment(self, document_id: str, attachment_data: Dict[str, Any]) -> Optional[DocumentAttachment]:
        """Adiciona um anexo a um documento"""
        data = self._load_data()
        
        for doc in data:
            if doc.get('id') == document_id:
                attachment = DocumentAttachment(attachment_data)
                doc['attachments'] = doc.get('attachments', [])
                doc['attachments'].append(attachment_data)
                self._save_data(data)
                return attachment
        
        return None
    
    def remove_attachment(self, document_id: str, attachment_id: str) -> bool:
        """Remove um anexo de um documento"""
        data = self._load_data()
        
        for doc in data:
            if doc.get('id') == document_id:
                attachments = doc.get('attachments', [])
                for i, attachment in enumerate(attachments):
                    if attachment.get('id') == attachment_id:
                        # Remove arquivo físico
                        file_path = attachment.get('file_path')
                        if file_path and os.path.exists(file_path):
                            try:
                                os.remove(file_path)
                            except OSError:
                                pass
                        
                        # Remove da lista
                        attachments.pop(i)
                        doc['attachments'] = attachments
                        self._save_data(data)
                        return True
        
        return False 