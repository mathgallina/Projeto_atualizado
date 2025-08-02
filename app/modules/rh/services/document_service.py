"""
Sistema RH isolado: não adicionar código que afete outras funcionalidades.
Qualquer alteração deve ser aprovada.
"""

import os
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from werkzeug.utils import secure_filename
from app.modules.rh.repositories.document_repository import DocumentRepository
from app.modules.rh.models import CorporateDocument, DocumentAttachment

class DocumentService:
    """Serviço para gerenciar documentos corporativos"""
    
    def __init__(self):
        self.document_repo = DocumentRepository()
        self.allowed_extensions = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif'}
    
    def get_all_documents(self) -> List[CorporateDocument]:
        """Retorna todos os documentos"""
        return self.document_repo.get_all()
    
    def get_document_by_id(self, document_id: str) -> Optional[CorporateDocument]:
        """Retorna um documento por ID"""
        return self.document_repo.get_by_id(document_id)
    
    def get_documents_by_employee(self, employee_id: str) -> List[CorporateDocument]:
        """Retorna documentos de um funcionário"""
        return self.document_repo.get_by_employee(employee_id)
    
    def get_documents_by_type(self, doc_type: str) -> List[CorporateDocument]:
        """Retorna documentos por tipo"""
        return self.document_repo.get_by_type(doc_type)
    
    def get_documents_by_department(self, department: str) -> List[CorporateDocument]:
        """Retorna documentos por departamento"""
        return self.document_repo.get_by_department(department)
    
    def search_documents(self, query: str) -> List[CorporateDocument]:
        """Busca documentos"""
        return self.document_repo.search(query)
    
    def create_document(self, document_data: Dict[str, Any]) -> CorporateDocument:
        """Cria um novo documento"""
        # Validações básicas
        if not document_data.get('title'):
            raise ValueError("Título é obrigatório")
        
        if not document_data.get('type'):
            raise ValueError("Tipo de documento é obrigatório")
        
        # Define valores padrão
        document_data['status'] = document_data.get('status', 'active')
        document_data['tags'] = document_data.get('tags', [])
        document_data['attachments'] = document_data.get('attachments', [])
        document_data['created_by'] = document_data.get('created_by', 'Sistema')
        
        return self.document_repo.create(document_data)
    
    def update_document(self, document_id: str, document_data: Dict[str, Any]) -> Optional[CorporateDocument]:
        """Atualiza um documento"""
        if not self.document_repo.get_by_id(document_id):
            raise ValueError("Documento não encontrado")
        
        document_data['updated_at'] = datetime.now().isoformat()
        return self.document_repo.update(document_id, document_data)
    
    def delete_document(self, document_id: str) -> bool:
        """Remove um documento"""
        return self.document_repo.delete(document_id)
    
    def upload_attachment(self, document_id: str, file, uploaded_by: str = 'Sistema') -> Optional[DocumentAttachment]:
        """Faz upload de um anexo para um documento"""
        if not file:
            raise ValueError("Arquivo é obrigatório")
        
        # Valida extensão
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in self.allowed_extensions:
            raise ValueError(f"Tipo de arquivo não permitido. Tipos aceitos: {', '.join(self.allowed_extensions)}")
        
        # Gera nome único para o arquivo
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(self.document_repo.attachments_dir, unique_filename)
        
        # Salva o arquivo
        file.save(file_path)
        
        # Cria dados do anexo
        attachment_data = {
            'id': str(uuid.uuid4()),
            'document_id': document_id,
            'filename': unique_filename,
            'original_filename': filename,
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'file_type': file_ext,
            'uploaded_by': uploaded_by,
            'uploaded_at': datetime.now().isoformat()
        }
        
        return self.document_repo.add_attachment(document_id, attachment_data)
    
    def remove_attachment(self, document_id: str, attachment_id: str) -> bool:
        """Remove um anexo de um documento"""
        return self.document_repo.remove_attachment(document_id, attachment_id)
    
    def get_document_with_employee(self, document_id: str) -> Optional[Dict]:
        """Retorna documento com informações do funcionário"""
        document = self.document_repo.get_by_id(document_id)
        if not document:
            return None
        
        return {
            'document': document,
            'employee': None  # Temporariamente desabilitado
        }
    
    def get_document_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas dos documentos"""
        documents = self.document_repo.get_all()
        
        total_documents = len(documents)
        active_documents = len([d for d in documents if d.status == 'active'])
        archived_documents = len([d for d in documents if d.status == 'archived'])
        draft_documents = len([d for d in documents if d.status == 'draft'])
        
        # Contagem por tipo
        types_count = {}
        for doc in documents:
            doc_type = doc.type
            types_count[doc_type] = types_count.get(doc_type, 0) + 1
        
        # Contagem por departamento
        departments_count = {}
        for doc in documents:
            dept = doc.department
            departments_count[dept] = departments_count.get(dept, 0) + 1
        
        return {
            'total_documents': total_documents,
            'active_documents': active_documents,
            'archived_documents': archived_documents,
            'draft_documents': draft_documents,
            'types_count': types_count,
            'departments_count': departments_count
        }
    
    def get_recent_documents(self, limit: int = 10) -> List[CorporateDocument]:
        """Retorna documentos mais recentes"""
        documents = self.document_repo.get_all()
        # Ordena por data de criação (mais recente primeiro)
        documents.sort(key=lambda x: x.created_at, reverse=True)
        return documents[:limit]
    
    def get_documents_by_status(self, status: str) -> List[CorporateDocument]:
        """Retorna documentos por status"""
        documents = self.document_repo.get_all()
        return [doc for doc in documents if doc.status == status] 