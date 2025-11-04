"""
Módulo base.py - Define a classe abstrata para todos os agentes.

Este módulo fornece a estrutura fundamental que todos os agentes especializados
herdam. Cada agente é responsável por uma tarefa específica na análise do aluno.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel


class AgentResponse(BaseModel):
    """
    Modelo que padroniza a resposta de cada agente.
    
    Atributos:
        agent_name: Nome do agente que gerou a resposta
        status: Status da execução ('sucesso' ou 'erro')
        resultado: O resultado principal da análise
        detalhes: Informações adicionais sobre o processo
    """
    agent_name: str
    status: str
    resultado: str
    detalhes: Optional[Dict[str, Any]] = None


class Agent(ABC):
    """
    Classe abstrata que define a interface para todos os agentes.
    
    Um agente é um especialista em uma tarefa específica. Todos os agentes
    devem herdar desta classe e implementar o método 'analisar'.
    """
    
    def __init__(self, nome: str):
        """
        Inicializa um agente.
        
        Args:
            nome: Nome único do agente
        """
        self.nome = nome
    
    @abstractmethod
    def analisar(self, dados: Dict[str, Any]) -> AgentResponse:
        """
        Método abstrato que cada agente deve implementar.
        
        Args:
            dados: Dicionário com os dados necessários para a análise
            
        Returns:
            AgentResponse: Resposta padronizada do agente
        """
        pass

