"""
Módulo engajamento.py - Analisador de Engajamento (Especialista em Frequência).

Este agente é responsável por analisar exclusivamente a presença e frequência
do aluno, identificando padrões de ausência e desengajamento.
"""

from typing import Dict, Any, List
from .base import Agent, AgentResponse


class AnalisadorEngajamento(Agent):
    """
    Especialista em análise de frequência e engajamento.
    
    Este agente examina:
    - Percentual de presença no semestre
    - Padrões de ausência
    - Disciplinas com maior ausência
    - Tendências de desengajamento
    """
    
    def agents(self):
        super().agents("Analisador de Engajamento")
    
    def analisar(self, dados: Dict[str, Any]) -> AgentResponse:
        """
        Analisa a frequência e engajamento do aluno.
        
        Args:
            dados: Dicionário contendo:
                - 'eventos': Lista de eventos de presença/ausência
                - 'disciplinas': Lista de disciplinas
                
        Returns:
            AgentResponse: Análise estruturada do engajamento
        """
        try:
            # Extrai os dados necessários
            eventos = dados.get('eventos', [])
            
            # Calcula o percentual de presença
            percentual_presenca = self._calcular_percentual_presenca(eventos)
            
            # Identifica padrões de ausência
            padroes_ausencia = self._identificar_padroes_ausencia(eventos)
            
            # Monta o resultado
            resultado = self._montar_resultado(percentual_presenca, padroes_ausencia)
            
            return AgentResponse(
                agent_name=self.nome,
                status="sucesso",
                resultado=resultado,
                detalhes={
                    "percentual_presenca": percentual_presenca,
                    "padroes_ausencia": padroes_ausencia
                }
            )
        
        except Exception as e:
            return AgentResponse(
                agent_name=self.nome,
                status="erro",
                resultado=f"Erro ao analisar engajamento: {str(e)}",
                detalhes={"erro": str(e)}
            )
    
    def _calcular_percentual_presenca(self, eventos: List[Dict[str, Any]]) -> float:
        """
        Calcula o percentual de presença baseado nos eventos.
        
        Args:
            eventos: Lista de eventos com informação de presença (0 ou 1)
            
        Returns:
            float: Percentual de presença (0-100)
        """
        if not eventos:
            return 0.0
        
        presencas = sum(1 for evento in eventos if evento.get('presenca', 0) == 1)
        total = len(eventos)
        
        return (presencas / total) * 100 if total > 0 else 0.0
    
    def _identificar_padroes_ausencia(self, eventos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identifica padrões de ausência nos eventos.
        
        Args:
            eventos: Lista de eventos
            
        Returns:
            Dict: Dicionário com informações sobre padrões de ausência
        """
        ausencias_por_disciplina = {}
        
        for evento in eventos:
            if evento.get('presenca', 0) == 0:
                disciplina = evento.get('disciplina', 'Desconhecida')
                if disciplina not in ausencias_por_disciplina:
                    ausencias_por_disciplina[disciplina] = 0
                ausencias_por_disciplina[disciplina] += 1
        
        return {
            "total_ausencias": sum(ausencias_por_disciplina.values()),
            "ausencias_por_disciplina": ausencias_por_disciplina
        }
    
    def _montar_resultado(self, percentual: float, padroes: Dict[str, Any]) -> str:
        """
        Monta o texto do resultado da análise.
        
        Args:
            percentual: Percentual de presença
            padroes: Dicionário com padrões de ausência
            
        Returns:
            str: Texto formatado do resultado
        """
        resultado = f"Frequência de presença: {percentual:.1f}%. "
        
        total_ausencias = padroes.get('total_ausencias', 0)
        if total_ausencias > 0:
            resultado += f"Total de ausências identificadas: {total_ausencias}. "
            
            ausencias_disciplina = padroes.get('ausencias_por_disciplina', {})
            if ausencias_disciplina:
                disciplina_maior_ausencia = max(ausencias_disciplina, key=ausencias_disciplina.get)
                resultado += f"Maior concentração de ausências em: {disciplina_maior_ausencia}."
        else:
            resultado += "Nenhuma ausência registrada."
        
        return resultado

