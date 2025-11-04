"""
Módulo desempenho.py - Analisador de Desempenho (Especialista em Notas).

Este agente é responsável por analisar exclusivamente as notas do aluno,
identificando tendências de queda, inconsistências e desempenho abaixo da média.
"""

from typing import Dict, Any, List
from .base import Agent, AgentResponse
import pandas as pd


class AnalisadorDesempenho(Agent):
    """
    Especialista em análise de notas e desempenho acadêmico.
    
    Este agente examina:
    - Média geral do semestre atual
    - Comparação com semestres anteriores
    - Queda de rendimento por disciplina
    - Desempenho abaixo da média
    """
    
    def __init__(self):
        super().__init__("Analisador de Desempenho")
    
    def analisar(self, dados: Dict[str, Any]) -> AgentResponse:
        """
        Analisa as notas do aluno e identifica padrões de desempenho.
        
        Args:
            dados: Dicionário contendo:
                - 'notas_atuais': Lista de notas do semestre atual
                - 'notas_anteriores': Lista de notas do semestre anterior
                - 'disciplinas': Lista de disciplinas com suas notas
                
        Returns:
            AgentResponse: Análise estruturada do desempenho
        """
        try:
            # Extrai os dados necessários
            notas_atuais = dados.get('notas_atuais', [])
            notas_anteriores = dados.get('notas_anteriores', [])
            disciplinas = dados.get('disciplinas', {})
            
            # Calcula a média geral do semestre atual
            media_atual = self._calcular_media(notas_atuais)
            
            # Calcula a média geral do semestre anterior
            media_anterior = self._calcular_media(notas_anteriores)
            
            # Identifica disciplinas críticas (notas baixas)
            disciplinas_criticas = self._identificar_disciplinas_criticas(disciplinas)
            
            # Calcula a queda de rendimento
            queda_rendimento = media_anterior - media_atual
            
            # Monta o resultado
            resultado = self._montar_resultado(
                media_atual,
                media_anterior,
                queda_rendimento,
                disciplinas_criticas
            )
            
            return AgentResponse(
                agent_name=self.nome,
                status="sucesso",
                resultado=resultado,
                detalhes={
                    "media_atual": media_atual,
                    "media_anterior": media_anterior,
                    "queda_rendimento": queda_rendimento,
                    "disciplinas_criticas": disciplinas_criticas
                }
            )
        
        except Exception as e:
            return AgentResponse(
                agent_name=self.nome,
                status="erro",
                resultado=f"Erro ao analisar desempenho: {str(e)}",
                detalhes={"erro": str(e)}
            )
    
    def _calcular_media(self, notas: List[float]) -> float:
        """
        Calcula a média aritmética de uma lista de notas.
        
        Args:
            notas: Lista de notas
            
        Returns:
            float: Média das notas (0.0 se lista vazia)
        """
        if not notas:
            return 0.0
        return sum(notas) / len(notas)
    
    def _identificar_disciplinas_criticas(self, disciplinas: Dict[str, List[float]]) -> List[str]:
        """
        Identifica disciplinas com desempenho crítico (média < 6.0).
        
        Args:
            disciplinas: Dicionário com nome da disciplina e suas notas
            
        Returns:
            List[str]: Lista de disciplinas críticas
        """
        criticas = []
        for disciplina, notas in disciplinas.items():
            media_disciplina = self._calcular_media(notas)
            if media_disciplina < 6.0:
                criticas.append(disciplina)
        return criticas
    
    def _montar_resultado(
        self,
        media_atual: float,
        media_anterior: float,
        queda: float,
        criticas: List[str]
    ) -> str:
        """
        Monta o texto do resultado da análise.
        
        Args:
            media_atual: Média do semestre atual
            media_anterior: Média do semestre anterior
            queda: Diferença entre as médias
            criticas: Disciplinas críticas
            
        Returns:
            str: Texto formatado do resultado
        """
        resultado = f"Detectada queda de {queda:.1f} pontos na média geral, "
        resultado += f"de {media_anterior:.1f} para {media_atual:.1f}. "
        
        if criticas:
            resultado += f"Disciplinas críticas identificadas: {', '.join(criticas)}."
        else:
            resultado += "Nenhuma disciplina com desempenho crítico."
        
        return resultado

