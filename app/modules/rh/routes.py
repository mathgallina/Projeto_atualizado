"""
Sistema RH isolado: não adicionar código que afete outras funcionalidades.
Qualquer alteração deve ser aprovada.
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from app.modules.rh.services.rh_service import RHService
from app.modules.rh.services.document_service import DocumentService
from datetime import datetime
import uuid
import os

rh_bp = Blueprint('rh', __name__, url_prefix='/rh')
rh_service = RHService()
document_service = DocumentService()

@rh_bp.route('/')
def index():
    """Página principal do RH"""
    stats = rh_service.get_dashboard_stats()
    return render_template('rh/index.html', stats=stats)

@rh_bp.route('/employees')
def employees():
    """Lista de funcionários"""
    employees = rh_service.get_all_employees()
    return render_template('rh/employees.html', employees=employees)

@rh_bp.route('/employees/create', methods=['GET', 'POST'])
def create_employee():
    """Criar novo funcionário"""
    if request.method == 'POST':
        try:
            employee_data = {
                'name': request.form['name'],
                'position': request.form['position'],
                'department': request.form['department'],
                'email': request.form['email'],
                'phone': request.form['phone'],
                'hire_date': request.form['hire_date'],
                'status': request.form.get('status', 'active'),
                'notes': request.form.get('notes')
            }
            
            employee = rh_service.create_employee(employee_data)
            flash('Funcionário criado com sucesso!', 'success')
            return redirect(url_for('rh.employees'))
            
        except Exception as e:
            flash(f'Erro ao criar funcionário: {str(e)}', 'error')
    
    return render_template('rh/create_employee.html')

@rh_bp.route('/employees/<employee_id>')
def view_employee(employee_id):
    """Visualizar funcionário"""
    employee_data = rh_service.get_employee_with_equipment(employee_id)
    if not employee_data:
        flash('Funcionário não encontrado', 'error')
        return redirect(url_for('rh.employees'))
    
    return render_template('rh/view_employee.html', data=employee_data)

@rh_bp.route('/employees/<employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Editar funcionário"""
    employee = rh_service.get_employee_by_id(employee_id)
    if not employee:
        flash('Funcionário não encontrado', 'error')
        return redirect(url_for('rh.employees'))
    
    if request.method == 'POST':
        try:
            employee_data = {
                'name': request.form['name'],
                'position': request.form['position'],
                'department': request.form['department'],
                'email': request.form['email'],
                'phone': request.form['phone'],
                'hire_date': request.form['hire_date'],
                'status': request.form.get('status', 'active'),
                'notes': request.form.get('notes')
            }
            
            updated_employee = rh_service.update_employee(employee_id, employee_data)
            if updated_employee:
                flash('Funcionário atualizado com sucesso!', 'success')
                return redirect(url_for('rh.view_employee', employee_id=employee_id))
            else:
                flash('Erro ao atualizar funcionário', 'error')
                
        except Exception as e:
            flash(f'Erro ao atualizar funcionário: {str(e)}', 'error')
    
    return render_template('rh/edit_employee.html', employee=employee)

@rh_bp.route('/employees/<employee_id>/delete', methods=['POST'])
def delete_employee(employee_id):
    """Deletar funcionário"""
    try:
        success = rh_service.delete_employee(employee_id)
        if success:
            flash('Funcionário removido com sucesso!', 'success')
        else:
            flash('Erro ao remover funcionário', 'error')
    except Exception as e:
        flash(f'Erro ao remover funcionário: {str(e)}', 'error')
    
    return redirect(url_for('rh.employees'))

@rh_bp.route('/equipment')
def equipment():
    """Lista de equipamentos"""
    equipment_list = rh_service.get_all_equipment()
    return render_template('rh/equipment.html', equipment=equipment_list)

@rh_bp.route('/equipment/create', methods=['GET', 'POST'])
def create_equipment():
    """Criar novo equipamento"""
    if request.method == 'POST':
        try:
            equipment_data = {
                'name': request.form['name'],
                'type': request.form['type'],
                'serial_number': request.form['serial_number'],
                'brand': request.form['brand'],
                'model': request.form['model'],
                'assigned_to': request.form['assigned_to'],
                'purchase_date': request.form['purchase_date'],
                'warranty_expiry': request.form['warranty_expiry'],
                'status': request.form.get('status', 'active'),
                'notes': request.form.get('notes')
            }
            
            equipment = rh_service.create_equipment(equipment_data)
            flash('Equipamento criado com sucesso!', 'success')
            return redirect(url_for('rh.equipment'))
            
        except Exception as e:
            flash(f'Erro ao criar equipamento: {str(e)}', 'error')
    
    employees = rh_service.get_active_employees()
    return render_template('rh/create_equipment.html', employees=employees)

@rh_bp.route('/equipment/<equipment_id>')
def view_equipment(equipment_id):
    """Visualizar equipamento"""
    equipment = rh_service.get_equipment_by_id(equipment_id)
    if not equipment:
        flash('Equipamento não encontrado', 'error')
        return redirect(url_for('rh.equipment'))
    
    assigned_employee = None
    if equipment.assigned_to:
        assigned_employee = rh_service.get_employee_by_id(equipment.assigned_to)
    
    return render_template('rh/view_equipment.html', equipment=equipment, employee=assigned_employee)

@rh_bp.route('/equipment/<equipment_id>/edit', methods=['GET', 'POST'])
def edit_equipment(equipment_id):
    """Editar equipamento"""
    equipment = rh_service.get_equipment_by_id(equipment_id)
    if not equipment:
        flash('Equipamento não encontrado', 'error')
        return redirect(url_for('rh.equipment'))
    
    if request.method == 'POST':
        try:
            equipment_data = {
                'name': request.form['name'],
                'type': request.form['type'],
                'serial_number': request.form['serial_number'],
                'brand': request.form['brand'],
                'model': request.form['model'],
                'assigned_to': request.form['assigned_to'],
                'purchase_date': request.form['purchase_date'],
                'warranty_expiry': request.form['warranty_expiry'],
                'status': request.form.get('status', 'active'),
                'notes': request.form.get('notes')
            }
            
            updated_equipment = rh_service.update_equipment(equipment_id, equipment_data)
            if updated_equipment:
                flash('Equipamento atualizado com sucesso!', 'success')
                return redirect(url_for('rh.view_equipment', equipment_id=equipment_id))
            else:
                flash('Erro ao atualizar equipamento', 'error')
                
        except Exception as e:
            flash(f'Erro ao atualizar equipamento: {str(e)}', 'error')
    
    employees = rh_service.get_active_employees()
    return render_template('rh/edit_equipment.html', equipment=equipment, employees=employees)

@rh_bp.route('/equipment/<equipment_id>/delete', methods=['POST'])
def delete_equipment(equipment_id):
    """Deletar equipamento"""
    try:
        success = rh_service.delete_equipment(equipment_id)
        if success:
            flash('Equipamento removido com sucesso!', 'success')
        else:
            flash('Erro ao remover equipamento', 'error')
    except Exception as e:
        flash(f'Erro ao remover equipamento: {str(e)}', 'error')
    
    return redirect(url_for('rh.equipment'))

@rh_bp.route('/search')
def search():
    """Busca em funcionários e equipamentos"""
    query = request.args.get('q', '')
    if not query:
        return render_template('rh/search.html', results=None)
    
    employees = rh_service.search_employees(query)
    equipment = rh_service.search_equipment(query)
    
    results = {
        'employees': employees,
        'equipment': equipment,
        'query': query
    }
    
    return render_template('rh/search.html', results=results)

@rh_bp.route('/reports')
def reports():
    """Relatórios do RH"""
    stats = rh_service.get_dashboard_stats()
    warranty_expiring = rh_service.get_warranty_expiring_soon(30)
    
    return render_template('rh/reports.html', stats=stats, warranty_expiring=warranty_expiring)

# APIs para AJAX
@rh_bp.route('/api/employees')
def api_employees():
    """API para listar funcionários"""
    employees = rh_service.get_all_employees()
    return jsonify([{
        'id': emp.id,
        'name': emp.name,
        'position': emp.position,
        'department': emp.department,
        'email': emp.email,
        'status': emp.status
    } for emp in employees])

@rh_bp.route('/api/equipment')
def api_equipment():
    """API para listar equipamentos"""
    equipment = rh_service.get_all_equipment()
    return jsonify([{
        'id': eq.id,
        'name': eq.name,
        'type': eq.type,
        'brand': eq.brand,
        'model': eq.model,
        'status': eq.status
    } for eq in equipment])

# Rotas para Documentos Corporativos
@rh_bp.route('/documents')
def documents():
    """Lista de documentos corporativos"""
    documents = document_service.get_all_documents()
    stats = document_service.get_document_stats()
    return render_template('rh/documents.html', documents=documents, stats=stats)

@rh_bp.route('/documents/create', methods=['GET', 'POST'])
def create_document():
    """Criar novo documento"""
    if request.method == 'POST':
        try:
            document_data = {
                'title': request.form['title'],
                'type': request.form['type'],
                'content': request.form['content'],
                'employee_id': request.form.get('employee_id', ''),
                'department': request.form.get('department', ''),
                'status': request.form.get('status', 'active'),
                'tags': request.form.get('tags', '').split(',') if request.form.get('tags') else [],
                'created_by': 'Sistema'
            }
            
            document = document_service.create_document(document_data)
            
            # Upload de anexos
            files = request.files.getlist('attachments')
            for file in files:
                if file and file.filename:
                    document_service.upload_attachment(document.id, file)
            
            flash('Documento criado com sucesso!', 'success')
            return redirect(url_for('rh.documents'))
            
        except Exception as e:
            flash(f'Erro ao criar documento: {str(e)}', 'error')
    
    employees = rh_service.get_active_employees()
    return render_template('rh/create_document.html', employees=employees)

@rh_bp.route('/documents/<document_id>')
def view_document(document_id):
    """Visualizar documento"""
    document_data = document_service.get_document_with_employee(document_id)
    if not document_data:
        flash('Documento não encontrado', 'error')
        return redirect(url_for('rh.documents'))
    
    return render_template('rh/view_document.html', data=document_data)

@rh_bp.route('/documents/<document_id>/edit', methods=['GET', 'POST'])
def edit_document(document_id):
    """Editar documento"""
    document = document_service.get_document_by_id(document_id)
    if not document:
        flash('Documento não encontrado', 'error')
        return redirect(url_for('rh.documents'))
    
    if request.method == 'POST':
        try:
            document_data = {
                'title': request.form['title'],
                'type': request.form['type'],
                'content': request.form['content'],
                'employee_id': request.form.get('employee_id', ''),
                'department': request.form.get('department', ''),
                'status': request.form.get('status', 'active'),
                'tags': request.form.get('tags', '').split(',') if request.form.get('tags') else []
            }
            
            updated_document = document_service.update_document(document_id, document_data)
            if updated_document:
                flash('Documento atualizado com sucesso!', 'success')
                return redirect(url_for('rh.view_document', document_id=document_id))
            else:
                flash('Erro ao atualizar documento', 'error')
                
        except Exception as e:
            flash(f'Erro ao atualizar documento: {str(e)}', 'error')
    
    employees = rh_service.get_active_employees()
    return render_template('rh/edit_document.html', document=document, employees=employees)

@rh_bp.route('/documents/<document_id>/delete', methods=['POST'])
def delete_document(document_id):
    """Deletar documento"""
    try:
        success = document_service.delete_document(document_id)
        if success:
            flash('Documento removido com sucesso!', 'success')
        else:
            flash('Erro ao remover documento', 'error')
    except Exception as e:
        flash(f'Erro ao remover documento: {str(e)}', 'error')
    
    return redirect(url_for('rh.documents'))

@rh_bp.route('/documents/<document_id>/upload', methods=['POST'])
def upload_attachment(document_id):
    """Upload de anexo para documento"""
    try:
        file = request.files.get('attachment')
        if file and file.filename:
            attachment = document_service.upload_attachment(document_id, file)
            if attachment:
                flash('Anexo adicionado com sucesso!', 'success')
            else:
                flash('Erro ao adicionar anexo', 'error')
        else:
            flash('Nenhum arquivo selecionado', 'error')
    except Exception as e:
        flash(f'Erro ao fazer upload: {str(e)}', 'error')
    
    return redirect(url_for('rh.view_document', document_id=document_id))

@rh_bp.route('/documents/<document_id>/attachment/<attachment_id>/delete', methods=['POST'])
def delete_attachment(document_id, attachment_id):
    """Deletar anexo"""
    try:
        success = document_service.remove_attachment(document_id, attachment_id)
        if success:
            flash('Anexo removido com sucesso!', 'success')
        else:
            flash('Erro ao remover anexo', 'error')
    except Exception as e:
        flash(f'Erro ao remover anexo: {str(e)}', 'error')
    
    return redirect(url_for('rh.view_document', document_id=document_id))

@rh_bp.route('/documents/<document_id>/attachment/<attachment_id>/download')
def download_attachment(document_id, attachment_id):
    """Download de anexo"""
    try:
        document = document_service.get_document_by_id(document_id)
        if not document:
            flash('Documento não encontrado', 'error')
            return redirect(url_for('rh.documents'))
        
        # Encontra o anexo
        attachment = None
        for att in document.attachments:
            if att.get('id') == attachment_id:
                attachment = att
                break
        
        if not attachment:
            flash('Anexo não encontrado', 'error')
            return redirect(url_for('rh.view_document', document_id=document_id))
        
        file_path = attachment.get('file_path')
        if not file_path or not os.path.exists(file_path):
            flash('Arquivo não encontrado', 'error')
            return redirect(url_for('rh.view_document', document_id=document_id))
        
        return send_file(file_path, as_attachment=True, download_name=attachment.get('original_filename'))
        
    except Exception as e:
        flash(f'Erro ao fazer download: {str(e)}', 'error')
        return redirect(url_for('rh.view_document', document_id=document_id))

@rh_bp.route('/documents/search')
def search_documents():
    """Busca em documentos"""
    query = request.args.get('q', '')
    if not query:
        return render_template('rh/search_documents.html', results=None)
    
    documents = document_service.search_documents(query)
    
    results = {
        'documents': documents,
        'query': query
    }
    
    return render_template('rh/search_documents.html', results=results) 