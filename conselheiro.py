"""
Módulo conselheiro.py - Conselheiro Acadêmico (O Estrategista).

Este agente recebe o diagnóstico final validado e escolhe a ação mais
precisa em um "playbook" de intervenções pedagógicas.
"""

from typing import Dict, Any
from .base import Agent, AgentResponse


class ConselheiroAcademico(Agent):
    """
    Especialista em recomendações e intervenções pedagógicas.
    
    Este agente:
    - Recebe o diagnóstico validado
    - Consulta um playbook de intervenções
    - Escolhe a ação mais apropriada
    - Monta a recomendação final
    """
    
    # Playbook de intervenções pedagógicas
    PLAYBOOK = {
        "PB_PEDAG_01": {
            "titulo": "Acompanhamento Geral Intensivo",
            "descricao": "Programa de acompanhamento semanal com coordenador",
            "canal": "Sistema Acadêmico / E-mail do Coordenador",
            "template": "ALERTA: Aluno [Nome] (ID: {id_aluno}) apresentou sinais de desengajamento geral. Sugestão: Acompanhamento semanal com o coordenador do curso."
        },
        "PB_PEDAG_02": {
            "titulo": "Agendar Reunião de Apoio Pedagógico Focado",
            "descricao": "Reunião com foco em disciplina específica",
            "canal": "Sistema Acadêmico / E-mail do Coordenador",
            "template": "ALERTA: Aluno [Nome] (ID: {id_aluno}) apresentou sinais de dificuldade pontual. Sugestão: Coordenador do curso deve convidá-lo para uma conversa e oferecer tutoria específica para a disciplina crítica."
        },
        "PB_PEDAG_03": {
            "titulo": "Oferecer Tutoria Especializada",
            "descricao": "Tutoria com especialista na disciplina",
            "canal": "Sistema Acadêmico / E-mail do Tutor",
            "template": "ALERTA: Aluno [Nome] (ID: {id_aluno}) necessita de tutoria especializada. Sugestão: Tutor deve entrar em contato para oferecer sessões de reforço."
        },
        "PB_PEDAG_04": {
            "titulo": "Avaliação Psicopedagógica",
            "descricao": "Encaminhamento para avaliação especializada",
            "canal": "Sistema Acadêmico / E-mail do Psicopedagogo",
            "template": "ALERTA: Aluno [Nome] (ID: {id_aluno}) apresenta sinais que sugerem necessidade de avaliação especializada. Sugestão: Encaminhar para psicopedagogo."
        }
    }
    
    def __init__(self):
        super().__init__("Conselheiro Acadêmico")
    
    def analisar(self, dados: Dict[str, Any]) -> AgentResponse:
        """
        Recomenda uma ação baseada no diagnóstico validado.
        
        Args:
            dados: Dicionário contendo:
                - 'diagnostico': Diagnóstico validado
                - 'id_aluno': ID do aluno
                - 'nome_aluno': Nome do aluno
                - 'detalhes_desempenho': Detalhes de desempenho
                - 'detalhes_engajamento': Detalhes de engajamento
                
        Returns:
            AgentResponse: Recomendação de ação
        """
        try:
            diagnostico = dados.get('diagnostico', '')
            id_aluno = dados.get('id_aluno', 'desconhecido')
            nome_aluno = dados.get('nome_aluno', 'Aluno')
            detalhes_desempenho = dados.get('detalhes_desempenho', {})
            detalhes_engajamento = dados.get('detalhes_engajamento', {})
            
            # Escolhe a ação apropriada
            acao = self._escolher_acao(
                diagnostico,
                detalhes_desempenho,
                detalhes_engajamento
            )
            
            # Monta a recomendação
            recomendacao = self._montar_recomendacao(acao, id_aluno, nome_aluno)
            
            return AgentResponse(
                agent_name=self.nome,
                status="sucesso",
                resultado=recomendacao['descricao'],
                detalhes={
                    "playbook_id": acao['playbook_id'],
                    "titulo": acao['titulo'],
                    "canal": acao['canal'],
                    "template_mensagem": acao['template_mensagem']
                }
            )
        
        except Exception as e:
            return AgentResponse(
                agent_name=self.nome,
                status="erro",
                resultado=f"Erro ao recomendar ação: {str(e)}",
                detalhes={"erro": str(e)}
            )
    
    def _escolher_acao(
        self,
        diagnostico: str,
        detalhes_desempenho: Dict[str, Any],
        detalhes_engajamento: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Escolhe a ação mais apropriada baseada no diagnóstico.
        
        Args:
            diagnostico: Diagnóstico do aluno
            detalhes_desempenho: Detalhes de desempenho
            detalhes_engajamento: Detalhes de engajamento
            
        Returns:
            Dict: Ação escolhida do playbook
        """
        queda_rendimento = detalhes_desempenho.get('queda_rendimento', 0)
        percentual_presenca = detalhes_engajamento.get('percentual_presenca', 100)
        disciplinas_criticas = detalhes_desempenho.get('disciplinas_criticas', [])
        
        # Lógica de escolha de ação
        if queda_rendimento > 3.0 and percentual_presenca < 50:
            # Situação crítica: desengajamento geral
            playbook_id = "PB_PEDAG_04"
        elif len(disciplinas_criticas) == 1 and percentual_presenca > 70:
            # Dificuldade específica em uma disciplina
            playbook_id = "PB_PEDAG_02"
        elif len(disciplinas_criticas) > 1 and percentual_presenca < 70:
            # Múltiplas disciplinas críticas com baixa frequência
            playbook_id = "PB_PEDAG_01"
        else:
            # Caso padrão: tutoria especializada
            playbook_id = "PB_PEDAG_03"
        
        playbook = self.PLAYBOOK.get(playbook_id, self.PLAYBOOK["PB_PEDAG_02"])
        
        return {
            "playbook_id": playbook_id,
            "titulo": playbook['titulo'],
            "canal": playbook['canal'],
            "template_mensagem": playbook['template']
        }
    
    def _montar_recomendacao(
        self,
        acao: Dict[str, str],
        id_aluno: str,
        nome_aluno: str
    ) -> Dict[str, str]:
        """
        Monta a recomendação final.
        
        Args:
            acao: Ação escolhida
            id_aluno: ID do aluno
            nome_aluno: Nome do aluno
            
        Returns:
            Dict: Recomendação formatada
        """
        template = acao['template_mensagem']
        template = template.replace('[Nome]', nome_aluno)
        template = template.replace('{id_aluno}', id_aluno)
        
        return {
            "descricao": f"Recomendação: {acao['titulo']}",
            "titulo": acao['titulo'],
            "canal": acao['canal'],
            "template_mensagem": template
        }

