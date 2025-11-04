"""
Pacote agents - Contém todos os agentes especializados do sistema.
"""

from .base import Agent, AgentResponse
from .desempenho import AnalisadorDesempenho
from .engajamento import AnalisadorEngajamento
from .diagnostico import AgenteDiagnostico
from .validador import ValidadorHipoteses
from .conselheiro import ConselheiroAcademico
from .coordenador import CoordenadorAnalise

__all__ = [
    'Agent',
    'AgentResponse',
    'AnalisadorDesempenho',
    'AnalisadorEngajamento',
    'AgenteDiagnostico',
    'ValidadorHipoteses',
    'ConselheiroAcademico',
    'CoordenadorAnalise'
]

