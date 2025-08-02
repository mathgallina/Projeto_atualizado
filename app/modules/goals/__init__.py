"""
Módulo de Sistema de Metas
Integração com o sistema de metas existente
"""

from flask import Blueprint

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

from . import routes 