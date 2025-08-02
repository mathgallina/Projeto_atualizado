"""
Rotas do Sistema de Treinamentos Internos
"""

import logging
import os
from flask import render_template, request, jsonify, current_app, redirect, url_for, flash, send_file, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import trainings_bp
from .repositories.training_repository import TrainingRepository

logger = logging.getLogger(__name__)

# Configuração para upload de arquivos
UPLOAD_FOLDER = 'app/static/uploads/trainings'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'mp4', 'avi', 'mov', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@trainings_bp.route('/')
@login_required
def index():
    """Página principal do sistema de treinamentos"""
    try:
        logger.info(f"Usuário {current_user.username} acessando sistema de treinamentos")
        
        # Usar repositório para carregar dados
        training_repo = TrainingRepository()
        categories = training_repo.get_all_categories()
        recent_trainings = training_repo.get_recent_trainings(limit=4)
        stats = training_repo.get_training_stats()
        
        return render_template(
            'trainings/index.html',
            categories=categories,
            recent_trainings=recent_trainings,
            stats=stats,
            current_user=current_user,
            active_page="trainings"
        )
        
    except Exception as e:
        logger.error(f"Erro no acesso ao sistema de treinamentos: {e}")
        return render_template('trainings/index.html', error="Erro ao carregar treinamentos")


@trainings_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_training():
    """Página para criar novo treinamento"""
    try:
        if request.method == 'POST':
            # Processar criação do treinamento
            training_data = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'category': request.form.get('category'),
                'duration': int(request.form.get('duration', 0)),
                'difficulty': request.form.get('difficulty'),
                'instructor': request.form.get('instructor'),
                'materials': [],
                'video_url': request.form.get('video_url'),
                'is_active': True
            }
            
            # Processar upload de materiais
            materials = request.files.getlist('materials')
            for material in materials:
                if material and allowed_file(material.filename):
                    filename = secure_filename(material.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    material.save(filepath)
                    training_data['materials'].append(filename)
            
            # Salvar treinamento
            training_repo = TrainingRepository()
            training_repo.create_training(training_data)
            
            flash('Treinamento criado com sucesso!', 'success')
            return redirect(url_for('trainings.index'))
        
        # GET: Mostrar formulário
        training_repo = TrainingRepository()
        categories = training_repo.get_all_categories()
        
        return render_template(
            'trainings/create.html',
            categories=categories,
            current_user=current_user,
            active_page="trainings"
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar treinamento: {e}")
        flash('Erro ao criar treinamento', 'error')
        return redirect(url_for('trainings.index'))


@trainings_bp.route('/edit/<training_id>', methods=['GET', 'POST'])
@login_required
def edit_training(training_id):
    """Editar treinamento existente"""
    try:
        training_repo = TrainingRepository()
        training = training_repo.get_training_by_id(training_id)
        
        if not training:
            flash('Treinamento não encontrado', 'error')
            return redirect(url_for('trainings.index'))
        
        if request.method == 'POST':
            # Processar edição do treinamento
            training_data = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'category': request.form.get('category'),
                'duration': int(request.form.get('duration', 0)),
                'difficulty': request.form.get('difficulty'),
                'instructor': request.form.get('instructor'),
                'materials': training.get('materials', []),
                'video_url': request.form.get('video_url'),
                'is_active': training.get('is_active', True)
            }
            
            # Processar upload de novos materiais
            materials = request.files.getlist('materials')
            for material in materials:
                if material and allowed_file(material.filename):
                    filename = secure_filename(material.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    material.save(filepath)
                    training_data['materials'].append(filename)
            
            # Atualizar treinamento
            training_repo.update_training(training_id, training_data)
            
            flash('Treinamento atualizado com sucesso!', 'success')
            return redirect(url_for('trainings.training_detail', training_id=training_id))
        
        # GET: Mostrar formulário de edição
        categories = training_repo.get_all_categories()
        
        return render_template(
            'trainings/edit.html',
            training=training,
            categories=categories,
            current_user=current_user
        )
        
    except Exception as e:
        logger.error(f"Erro ao editar treinamento {training_id}: {e}")
        flash('Erro ao editar treinamento', 'error')
        return redirect(url_for('trainings.index'))


@trainings_bp.route('/delete/<training_id>')
@login_required
def delete_training(training_id):
    """Excluir treinamento"""
    try:
        training_repo = TrainingRepository()
        training = training_repo.get_training_by_id(training_id)
        
        if not training:
            flash('Treinamento não encontrado', 'error')
            return redirect(url_for('trainings.index'))
        
        # Excluir treinamento
        training_repo.delete_training(training_id)
        
        flash('Treinamento excluído com sucesso!', 'success')
        return redirect(url_for('trainings.admin_dashboard'))
        
    except Exception as e:
        logger.error(f"Erro ao excluir treinamento {training_id}: {e}")
        flash('Erro ao excluir treinamento', 'error')
        return redirect(url_for('trainings.index'))


@trainings_bp.route('/admin')
@login_required
def admin_dashboard():
    """Dashboard administrativo para gestão de treinamentos"""
    try:
        training_repo = TrainingRepository()
        all_trainings = training_repo.get_all_trainings()
        categories = training_repo.get_all_categories()
        stats = training_repo.get_training_stats()
        
        return render_template(
            'trainings/admin.html',
            trainings=all_trainings,
            categories=categories,
            stats=stats,
            current_user=current_user,
            active_page="trainings"
        )
        
    except Exception as e:
        logger.error(f"Erro no dashboard administrativo: {e}")
        flash('Erro ao carregar dashboard administrativo', 'error')
        return redirect(url_for('trainings.index'))


@trainings_bp.route('/training/<training_id>')
@login_required
def training_detail(training_id):
    """Página de detalhes de um treinamento específico"""
    try:
        logger.info(f"Usuário {current_user.username} acessando treinamento {training_id}")
        
        training_repo = TrainingRepository()
        training = training_repo.get_training_by_id(training_id)
        
        if not training:
            flash('Treinamento não encontrado', 'error')
            return redirect(url_for('trainings.index'))
        
        # Buscar progresso do usuário atual
        user_progress = training_repo.get_training_progress(str(current_user.id), training_id)
        
        return render_template(
            'trainings/detail.html',
            training=training,
            user_progress=user_progress,
            current_user=current_user,
            active_page="trainings"
        )
        
    except Exception as e:
        logger.error(f"Erro ao acessar treinamento {training_id}: {e}")
        return render_template('trainings/detail.html', error="Erro ao carregar treinamento")


@trainings_bp.route('/category/<category_id>')
@login_required
def category(category_id):
    """Página de uma categoria específica de treinamentos"""
    try:
        logger.info(f"Usuário {current_user.username} acessando categoria {category_id}")
        
        training_repo = TrainingRepository()
        category_data = training_repo.get_category_by_id(category_id)
        trainings = training_repo.get_trainings_by_category(category_id)
        
        if not category_data:
            flash('Categoria não encontrada', 'error')
            return redirect(url_for('trainings.index'))
        
        return render_template(
            'trainings/category.html',
            category=category_data,
            trainings=trainings,
            current_user=current_user,
            active_page="trainings"
        )
        
    except Exception as e:
        logger.error(f"Erro ao acessar categoria {category_id}: {e}")
        return render_template('trainings/category.html', error="Erro ao carregar categoria")


@trainings_bp.route('/present/<filename>')
@login_required
def present_material(filename):
    """Apresentar material (PDF) em tela cheia"""
    try:
        # Corrigir o caminho do arquivo
        file_path = os.path.join(os.getcwd(), 'app/static/uploads/trainings', filename)
        
        if os.path.exists(file_path):
            # Determinar o tipo de conteúdo
            file_ext = filename.rsplit('.', 1)[1].lower()
            
            if file_ext == 'pdf':
                return render_template('trainings/present.html', filename=filename, active_page="trainings")
            else:
                return f"Arquivo não é um PDF: {filename}", 400
        else:
            logger.error(f"Arquivo não encontrado: {file_path}")
            return f"Arquivo não encontrado: {file_path}", 404
    except Exception as e:
        logger.error(f"Erro ao apresentar arquivo {filename}: {e}")
        return f"Erro ao apresentar arquivo: {str(e)}", 500

@trainings_bp.route('/view/<filename>')
@login_required
def view_material(filename):
    """Visualizar material (PDF, imagem, etc.)"""
    try:
        # Corrigir o caminho do arquivo
        file_path = os.path.join(os.getcwd(), 'app/static/uploads/trainings', filename)
        
        if os.path.exists(file_path):
            # Determinar o tipo de conteúdo
            file_ext = filename.rsplit('.', 1)[1].lower()
            
            if file_ext == 'pdf':
                response = send_file(file_path, mimetype='application/pdf')
                response.headers['Content-Disposition'] = 'inline'
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                return response
            elif file_ext in ['jpg', 'jpeg', 'png']:
                return send_file(file_path, mimetype=f'image/{file_ext}')
            else:
                # Para outros tipos, fazer download
                return send_file(file_path, as_attachment=True)
        else:
            logger.error(f"Arquivo não encontrado: {file_path}")
            return f"Arquivo não encontrado: {file_path}", 404
    except Exception as e:
        logger.error(f"Erro ao visualizar arquivo {filename}: {e}")
        return f"Erro ao visualizar arquivo: {str(e)}", 500


@trainings_bp.route('/download/<filename>')
@login_required
def download_material(filename):
    """Download de material de treinamento"""
    try:
        file_path = os.path.join(os.getcwd(), 'app/static/uploads/trainings', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            logger.error(f"Arquivo não encontrado: {file_path}")
            flash('Arquivo não encontrado', 'error')
            return redirect(request.referrer or url_for('trainings.index'))
    except Exception as e:
        logger.error(f"Erro ao fazer download do arquivo {filename}: {e}")
        flash('Erro ao fazer download', 'error')
        return redirect(request.referrer or url_for('trainings.index'))


@trainings_bp.route('/start/<training_id>')
@login_required
def start_training(training_id):
    """Iniciar um treinamento"""
    try:
        training_repo = TrainingRepository()
        training = training_repo.get_training_by_id(training_id)
        
        if not training:
            flash('Treinamento não encontrado', 'error')
            return redirect(url_for('trainings.index'))
        
        # Criar ou atualizar progresso do usuário
        training_repo.update_progress(
            str(current_user.id),
            training_id,
            {
                'progress_percentage': 10,  # Iniciar com 10%
                'completed_modules': ['started'],
                'started_at': 'now'
            }
        )
        
        flash('Treinamento iniciado com sucesso!', 'success')
        return redirect(url_for('trainings.training_detail', training_id=training_id))
        
    except Exception as e:
        logger.error(f"Erro ao iniciar treinamento {training_id}: {e}")
        flash('Erro ao iniciar treinamento', 'error')
        return redirect(url_for('trainings.index'))


@trainings_bp.route('/complete/<training_id>')
@login_required
def complete_training(training_id):
    """Marcar treinamento como concluído"""
    try:
        training_repo = TrainingRepository()
        training = training_repo.get_training_by_id(training_id)
        
        if not training:
            flash('Treinamento não encontrado', 'error')
            return redirect(url_for('trainings.index'))
        
        # Marcar como concluído
        training_repo.update_progress(
            str(current_user.id),
            training_id,
            {
                'progress_percentage': 100,
                'completed_modules': ['completed'],
                'completed_at': 'now'
            }
        )
        
        flash('Treinamento concluído com sucesso!', 'success')
        return redirect(url_for('trainings.training_detail', training_id=training_id))
        
    except Exception as e:
        logger.error(f"Erro ao concluir treinamento {training_id}: {e}")
        flash('Erro ao concluir treinamento', 'error')
        return redirect(url_for('trainings.index'))


@trainings_bp.route('/certificate/<training_id>')
@login_required
def generate_certificate(training_id):
    """Gerar certificado do treinamento"""
    try:
        training_repo = TrainingRepository()
        training = training_repo.get_training_by_id(training_id)
        user_progress = training_repo.get_training_progress(str(current_user.id), training_id)
        
        if not training:
            flash('Treinamento não encontrado', 'error')
            return redirect(url_for('trainings.index'))
        
        if not user_progress or user_progress.get('progress_percentage', 0) < 100:
            flash('Você precisa completar o treinamento para gerar o certificado', 'error')
            return redirect(url_for('trainings.training_detail', training_id=training_id))
        
        # Aqui você pode implementar a geração real do certificado
        # Por enquanto, vamos apenas mostrar uma mensagem
        flash('Certificado gerado com sucesso! (Funcionalidade em desenvolvimento)', 'success')
        return redirect(url_for('trainings.training_detail', training_id=training_id))
        
    except Exception as e:
        logger.error(f"Erro ao gerar certificado para treinamento {training_id}: {e}")
        flash('Erro ao gerar certificado', 'error')
        return redirect(url_for('trainings.index'))


@trainings_bp.route('/api/trainings')
@login_required
def api_trainings():
    """API para listar treinamentos"""
    try:
        training_repo = TrainingRepository()
        trainings = training_repo.get_all_trainings()
        
        return jsonify({
            'success': True,
            'trainings': trainings
        })
        
    except Exception as e:
        logger.error(f"Erro na API de treinamentos: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao carregar treinamentos'
        }), 500


@trainings_bp.route('/api/progress', methods=['POST'])
@login_required
def update_progress():
    """API para atualizar progresso do usuário"""
    try:
        data = request.get_json()
        training_id = data.get('training_id')
        progress_percentage = data.get('progress_percentage', 0)
        completed_modules = data.get('completed_modules', [])
        
        training_repo = TrainingRepository()
        training_repo.update_progress(
            str(current_user.id),
            training_id,
            {
                'progress_percentage': progress_percentage,
                'completed_modules': completed_modules
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Progresso atualizado com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao atualizar progresso: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao atualizar progresso'
        }), 500 