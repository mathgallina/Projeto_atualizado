"""
Rotas do Sistema de Metas Integrado
"""

import logging
from flask import render_template, request, jsonify, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
from . import goals_bp

logger = logging.getLogger(__name__)


@goals_bp.route('/')
@login_required
def index():
    """Página principal do sistema de metas integrado"""
    try:
        logger.info(f"Usuário {current_user.username} acessando sistema de metas integrado")
        
        # Carregar dados do sistema de metas existente
        from app.core.config import config
        from app.core.database import DatabaseManager
        from app.modules.goals.services.goals_service import GoalsService
        
        # Inicializar serviços
        db_manager = DatabaseManager(config['default'])
        goals_service = GoalsService(db_manager)
        
        # Buscar dados do sistema existente
        goals_data = goals_service.get_goals_dashboard_data()
        
        return render_template(
            'goals/index.html',
            goals_data=goals_data,
            current_user=current_user,
            active_page="goals"
        )
        
    except Exception as e:
        logger.error(f"Erro no acesso ao sistema de metas integrado: {e}")
        return render_template('goals/index.html', error="Erro ao carregar metas")


@goals_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard detalhado de metas"""
    try:
        from app.core.config import config
        from app.core.database import DatabaseManager
        from app.modules.goals.services.goals_service import GoalsService
        
        db_manager = DatabaseManager(config['default'])
        goals_service = GoalsService(db_manager)
        
        dashboard_data = goals_service.get_detailed_dashboard()
        
        return render_template(
            'goals/dashboard.html',
            dashboard_data=dashboard_data,
            current_user=current_user,
            active_page="goals"
        )
        
    except Exception as e:
        logger.error(f"Erro no dashboard de metas: {e}")
        return render_template('goals/dashboard.html', error="Erro ao carregar dashboard")


@goals_bp.route('/api/goals')
@login_required
def api_goals():
    """API para buscar metas"""
    try:
        from app.core.config import config
        from app.core.database import DatabaseManager
        from app.modules.goals.services.goals_service import GoalsService
        
        db_manager = DatabaseManager(config['default'])
        goals_service = GoalsService(db_manager)
        
        goals = goals_service.get_all_goals()
        
        return jsonify({
            "success": True,
            "data": goals
        })
        
    except Exception as e:
        logger.error(f"Erro na API de metas: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500 