"""
Módulo validador.py - Validador de Hipóteses (O Advogado do Diabo).

Este agente recebe a hipótese do Agente de Diagnóstico e tenta refutá-la
ou confirmá-la, adicionando nuances importantes à análise.
"""

from typing import Dict, Any
from .base import Agent, AgentResponse


class ValidadorHipoteses(Agent):
    """
    Especialista em validação crítica de hipóteses.
    
    Este agente:
    - Recebe a hipótese do diagnóstico
    - Analisa os dados brutos para tentar refutar
    - Adiciona nuances e contexto
    - Confirma ou refina a hipótese
    """
    
    def agents(self):
        super().agents("Validador de Hipóteses")
    
    def analisar(self, dados: Dict[str, Any]) -> AgentResponse:
        """
        Valida a hipótese diagnóstica através de análise crítica.
        
        Args:
            dados: Dicionário contendo:
                - 'hipotese': Hipótese do Agente de Diagnóstico
                - 'detalhes_desempenho': Detalhes da análise de desempenho
                - 'detalhes_engajamento': Detalhes da análise de engajamento
                
        Returns:
            AgentResponse: Validação e refinamento da hipótese
        """
        try:
            hipotese = dados.get('hipotese', '')
            detalhes_desempenho = dados.get('detalhes_desempenho', {})
            detalhes_engajamento = dados.get('detalhes_engajamento', {})
            
            # Valida a hipótese
            validacao = self._validar_hipotese(
                hipotese,
                detalhes_desempenho,
                detalhes_engajamento
            )
            
            return AgentResponse(
                agent_name=self.nome,
                status="sucesso",
                resultado=validacao['resultado'],
                detalhes={
                    "confirmada": validacao['confirmada'],
                    "nuances": validacao['nuances'],
                    "evidencias": validacao['evidencias']
                }
            )
        
        except Exception as e:
            return AgentResponse(
                agent_name=self.nome,
                status="erro",
                resultado=f"Erro ao validar hipótese: {str(e)}",
                detalhes={"erro": str(e)}
            )
    
    def _validar_hipotese(
        self,
        hipotese: str,
        detalhes_desempenho: Dict[str, Any],
        detalhes_engajamento: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Valida a hipótese e adiciona nuances.
        
        Args:
            hipotese: Hipótese a ser validada
            detalhes_desempenho: Detalhes de desempenho
            detalhes_engajamento: Detalhes de engajamento
            
        Returns:
            Dict: Resultado da validação com nuances
        """
        confirmada = True
        nuances = []
        evidencias = []
        
        # Extrai dados para análise
        queda_rendimento = detalhes_desempenho.get('queda_rendimento', 0)
        percentual_presenca = detalhes_engajamento.get('percentual_presenca', 100)
        disciplinas_criticas = detalhes_desempenho.get('disciplinas_criticas', [])
        ausencias_disciplina = detalhes_engajamento.get('padroes_ausencia', {}).get('ausencias_por_disciplina', {})
        
        # Lógica de validação
        if "desengajamento geral" in hipotese.lower():
            # Tenta refutar: verifica se é realmente geral
            if len(disciplinas_criticas) == 1 and percentual_presenca > 60:
                confirmada = False
                nuances.append("A hipótese de desengajamento geral é questionável. O problema parece concentrado em uma disciplina específica.")
            else:
                evidencias.append(f"Queda de {queda_rendimento:.1f} pontos confirma desempenho reduzido.")
                evidencias.append(f"Frequência de {percentual_presenca:.1f}% indica baixo engajamento.")
        
        elif "dificuldade específica" in hipotese.lower():
            # Valida: verifica se realmente é específica
            if len(disciplinas_criticas) > 1:
                nuances.append("Múltiplas disciplinas críticas sugerem que o problema pode ser mais amplo que uma dificuldade específica.")
            else:
                evidencias.append(f"Disciplinas críticas identificadas: {', '.join(disciplinas_criticas)}")
                if disciplinas_criticas[0] in ausencias_disciplina:
                    evidencias.append(f"Ausências concentradas em {disciplinas_criticas[0]} reforçam a hipótese.")
        
        # Monta o resultado
        resultado = f"Hipótese validada: {confirmada}. "
        if nuances:
            resultado += f"Nuances: {' '.join(nuances)} "
        if evidencias:
            resultado += f"Evidências: {' '.join(evidencias)}"
        
        return {
            "resultado": resultado,
            "confirmada": confirmada,
            "nuances": nuances,
            "evidencias": evidencias
        }

