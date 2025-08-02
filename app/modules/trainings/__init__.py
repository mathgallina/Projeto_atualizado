"""
Módulo de Treinamentos Internos - Veloz Fibra
Sistema para gerenciamento de treinamentos e capacitações internas
"""

from flask import Blueprint

trainings_bp = Blueprint('trainings', __name__, url_prefix='/trainings')

from . import routes 