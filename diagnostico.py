"""
Módulo diagnostico.py - Agente de Diagnóstico (O Médico).

Este agente recebe os relatórios dos dois analistas (Desempenho e Engajamento)
e formula uma hipótese inicial sobre a situação do aluno.
"""

from typing import Dict, Any
from .base import Agent, AgentResponse


class AgenteDiagnostico(Agent):
    """
    Especialista em formular hipóteses diagnósticas.
    
    Este agente:
    - Recebe relatórios dos analistas de desempenho e engajamento
    - Sintetiza as informações
    - Formula uma hipótese inicial sobre o problema
    - Prepara o diagnóstico para validação
    """
    
    def __init__(self):
        super().__init__("Agente de Diagnóstico")
    
    def analisar(self, dados: Dict[str, Any]) -> AgentResponse:
        """
        Formula uma hipótese diagnóstica baseada nos relatórios dos analistas.
        
        Args:
            dados: Dicionário contendo:
                - 'relatorio_desempenho': Resposta do AnalisadorDesempenho
                - 'relatorio_engajamento': Resposta do AnalisadorEngajamento
                - 'detalhes_desempenho': Detalhes da análise de desempenho
                - 'detalhes_engajamento': Detalhes da análise de engajamento
                
        Returns:
            AgentResponse: Hipótese diagnóstica
        """
        try:
            # Extrai os relatórios dos analistas
            detalhes_desempenho = dados.get('detalhes_desempenho', {})
            detalhes_engajamento = dados.get('detalhes_engajamento', {})
            
            # Analisa os padrões
            hipotese = self._formular_hipotese(detalhes_desempenho, detalhes_engajamento)
            
            return AgentResponse(
                agent_name=self.nome,
                status="sucesso",
                resultado=hipotese,
                detalhes={
                    "desempenho": detalhes_desempenho,
                    "engajamento": detalhes_engajamento
                }
            )
        
        except Exception as e:
            return AgentResponse(
                agent_name=self.nome,
                status="erro",
                resultado=f"Erro ao formular diagnóstico: {str(e)}",
                detalhes={"erro": str(e)}
            )
    
    def _formular_hipotese(
        self,
        detalhes_desempenho: Dict[str, Any],
        detalhes_engajamento: Dict[str, Any]
    ) -> str:
        """
        Formula a hipótese diagnóstica baseada nos dados.
        
        Args:
            detalhes_desempenho: Detalhes da análise de desempenho
            detalhes_engajamento: Detalhes da análise de engajamento
            
        Returns:
            str: Hipótese diagnóstica
        """
        queda_rendimento = detalhes_desempenho.get('queda_rendimento', 0)
        percentual_presenca = detalhes_engajamento.get('percentual_presenca', 100)
        disciplinas_criticas = detalhes_desempenho.get('disciplinas_criticas', [])
        ausencias_disciplina = detalhes_engajamento.get('padroes_ausencia', {}).get('ausencias_por_disciplina', {})
        
        # Lógica para formular a hipótese
        if queda_rendimento > 2.0 and percentual_presenca < 70:
            # Queda significativa e baixa frequência geral
            hipotese = "Queda de rendimento geral por desengajamento."
        elif disciplinas_criticas and len(disciplinas_criticas) == 1:
            # Problema concentrado em uma disciplina
            disciplina_problema = disciplinas_criticas[0]
            if disciplina_problema in ausencias_disciplina:
                hipotese = f"Dificuldade específica em {disciplina_problema} com ausências concentradas."
            else:
                hipotese = f"Dificuldade específica em {disciplina_problema}."
        elif queda_rendimento > 1.5:
            # Queda moderada
            hipotese = "Queda de rendimento com padrão de ausências seletivas."
        else:
            # Desempenho estável ou leve queda
            hipotese = "Desempenho relativamente estável com possível desengajamento em disciplinas específicas."
        
        return hipotese

