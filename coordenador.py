"""
Módulo coordenador.py - Coordenador de Análise (O Maestro).

Este agente gerencia todo o fluxo de análise. Ele:
1. Recebe o ID do aluno
2. Convoca os especialistas em paralelo
3. Coleta os resultados
4. Orquestra a validação
5. Monta o relatório final
"""

from typing import Dict, Any, List
import pandas as pd
from datetime import datetime
from .base import Agent, AgentResponse
from .desempenho import AnalisadorDesempenho
from .engajamento import AnalisadorEngajamento
from .diagnostico import AgenteDiagnostico
from .validador import ValidadorHipoteses
from .conselheiro import ConselheiroAcademico

class CoordenadorAnalise(Agent):
    """
    Maestro que orquestra toda a análise multiagente.
    
    Este agente:
    - Gerencia o fluxo de dados entre os agentes
    - Executa análises em paralelo quando possível
    - Consolida resultados
    - Monta o JSON final
    """
    
    def __init__(self, caminho_dataset: str):
        """
        Inicializa o coordenador.
        
        Args:
            caminho_dataset: Caminho para o arquivo CSV com dados dos alunos
        """
        super().__init__("Coordenador de Análise")
        self.caminho_dataset = caminho_dataset
        self.df = None
        self._carregar_dataset()
        
        # Inicializa os agentes especializados
        self.analisador_desempenho = AnalisadorDesempenho()
        self.analisador_engajamento = AnalisadorEngajamento()
        self.agente_diagnostico = AgenteDiagnostico()
        self.validador_hipoteses = ValidadorHipoteses()
        self.conselheiro_academico = ConselheiroAcademico()
    
    def _carregar_dataset(self):
        """Carrega o dataset CSV."""
        try:
            self.df = pd.read_csv(self.caminho_dataset)
        except Exception as e:
            raise Exception(f"Erro ao carregar dataset: {str(e)}")
    
    def analisar(self, dados: Dict[str, Any]) -> AgentResponse:
        """
        Orquestra a análise completa de um aluno.
        
        Args:
            dados: Dicionário contendo:
                - 'id_aluno': ID do aluno a analisar
                
        Returns:
            AgentResponse: Resultado completo da análise
        """
        try:
            id_aluno = dados.get('id_aluno')
            
            if not id_aluno:
                raise ValueError("ID do aluno não fornecido")
            
            # Extrai dados do aluno
            dados_aluno = self._extrair_dados_aluno(id_aluno)
            
            if not dados_aluno:
                raise ValueError(f"Aluno {id_aluno} não encontrado")
            
            # Executa análises em paralelo (simulado sequencialmente)
            resultado_desempenho = self.analisador_desempenho.analisar(
                dados_aluno['dados_desempenho']
            )
            
            resultado_engajamento = self.analisador_engajamento.analisar(
                dados_aluno['dados_engajamento']
            )
            
            # Formular diagnóstico
            resultado_diagnostico = self.agente_diagnostico.analisar({
                'relatorio_desempenho': resultado_desempenho,
                'relatorio_engajamento': resultado_engajamento,
                'detalhes_desempenho': resultado_desempenho.detalhes,
                'detalhes_engajamento': resultado_engajamento.detalhes
            })
            
            # Validar hipótese
            resultado_validacao = self.validador_hipoteses.analisar({
                'hipotese': resultado_diagnostico.resultado,
                'detalhes_desempenho': resultado_desempenho.detalhes,
                'detalhes_engajamento': resultado_engajamento.detalhes
            })
            
            # Recomendar ação
            resultado_acao = self.conselheiro_academico.analisar({
                'diagnostico': resultado_validacao.resultado,
                'id_aluno': id_aluno,
                'nome_aluno': dados_aluno['nome_aluno'],
                'detalhes_desempenho': resultado_desempenho.detalhes,
                'detalhes_engajamento': resultado_engajamento.detalhes
            })
            
            # Monta o JSON final
            json_final = self._montar_json_final(
                id_aluno,
                dados_aluno,
                resultado_desempenho,
                resultado_engajamento,
                resultado_diagnostico,
                resultado_validacao,
                resultado_acao
            )
            
            return AgentResponse(
                agent_name=self.nome,
                status="sucesso",
                resultado="Análise completa realizada com sucesso",
                detalhes=json_final
            )
        
        except Exception as e:
            return AgentResponse(
                agent_name=self.nome,
                status="erro",
                resultado=f"Erro na orquestração: {str(e)}",
                detalhes={"erro": str(e)}
            )
    
    def _extrair_dados_aluno(self, id_aluno: str) -> Dict[str, Any]:
        """
        Extrai todos os dados relevantes do aluno.
        
        Args:
            id_aluno: ID do aluno
            
        Returns:
            Dict: Dados estruturados do aluno
        """
        # Filtra dados do aluno
        dados_aluno_df = self.df[self.df['id_aluno'] == id_aluno]
        
        if dados_aluno_df.empty:
            return None
        
        # Extrai informações básicas
        nome_aluno = dados_aluno_df['nome_aluno'].iloc[0]
        
        # Separa por semestre
        semestre_atual = dados_aluno_df['semestre_letivo'].max()
        semestres_anteriores = dados_aluno_df[
            dados_aluno_df['semestre_letivo'] < semestre_atual
        ]
        
        # Extrai notas
        notas_atuais = dados_aluno_df[
            (dados_aluno_df['semestre_letivo'] == semestre_atual) &
            (dados_aluno_df['tipo_evento'] == 'prova') &
            (dados_aluno_df['nota'].notna())
        ]['nota'].tolist()
        
        notas_anteriores = semestres_anteriores[
            (semestres_anteriores['tipo_evento'] == 'prova') &
            (semestres_anteriores['nota'].notna())
        ]['nota'].tolist()
        
        # Extrai disciplinas e suas notas
        disciplinas = {}
        for disciplina in dados_aluno_df['id_disciplina'].unique():
            notas_disciplina = dados_aluno_df[
                (dados_aluno_df['id_disciplina'] == disciplina) &
                (dados_aluno_df['tipo_evento'] == 'prova') &
                (dados_aluno_df['nota'].notna())
            ]['nota'].tolist()
            if notas_disciplina:
                disciplinas[disciplina] = notas_disciplina
        
        # Extrai eventos de presença
        eventos = []
        for _, row in dados_aluno_df[
            dados_aluno_df['tipo_evento'] == 'aula'
        ].iterrows():
            eventos.append({
                'presenca': row['presenca'],
                'disciplina': row['id_disciplina'],
                'data': row['data_evento']
            })
        
        return {
            'nome_aluno': nome_aluno,
            'semestre_atual': semestre_atual,
            'dados_desempenho': {
                'notas_atuais': notas_atuais,
                'notas_anteriores': notas_anteriores,
                'disciplinas': disciplinas
            },
            'dados_engajamento': {
                'eventos': eventos
            }
        }
    
    def _montar_json_final(
        self,
        id_aluno: str,
        dados_aluno: Dict[str, Any],
        resultado_desempenho: AgentResponse,
        resultado_engajamento: AgentResponse,
        resultado_diagnostico: AgentResponse,
        resultado_validacao: AgentResponse,
        resultado_acao: AgentResponse
    ) -> Dict[str, Any]:
        """
        Monta o JSON final com toda a análise.
        
        Args:
            id_aluno: ID do aluno
            dados_aluno: Dados do aluno
            resultado_desempenho: Resultado do analisador de desempenho
            resultado_engajamento: Resultado do analisador de engajamento
            resultado_diagnostico: Resultado do diagnóstico
            resultado_validacao: Resultado da validação
            resultado_acao: Resultado da ação recomendada
            
        Returns:
            Dict: JSON final estruturado
        """
        # Calcula score de risco de evasão (0-100)
        score_risco = self._calcular_score_risco(
            resultado_desempenho.detalhes,
            resultado_engajamento.detalhes
        )
        
        # Determina diagnóstico chave
        diagnostico_chave = self._determinar_diagnostico_chave(
            resultado_validacao.detalhes
        )
        
        # Monta a justificativa
        justificativa = resultado_validacao.resultado
        
        return {
            "idAluno": id_aluno,
            "dataAnalise": datetime.utcnow().isoformat() + "Z",
            "scoreRiscoEvasao": score_risco,
            "diagnosticoChave": diagnostico_chave,
            "justificativa": justificativa,
            "processoDeAnalise": {
                "relatorioDesempenho": resultado_desempenho.resultado,
                "relatorioEngajamento": resultado_engajamento.resultado,
                "hipoteseInicial": resultado_diagnostico.resultado,
                "validacaoDaHipotese": resultado_validacao.resultado
            },
            "metricasAluno": {
                "mediaGeralSemestreAtual": round(
                    sum(dados_aluno['dados_desempenho']['notas_atuais']) / 
                    len(dados_aluno['dados_desempenho']['notas_atuais']), 1
                ) if dados_aluno['dados_desempenho']['notas_atuais'] else 0.0,
                "mediaGeralSemestreAnterior": round(
                    sum(dados_aluno['dados_desempenho']['notas_anteriores']) / 
                    len(dados_aluno['dados_desempenho']['notas_anteriores']), 1
                ) if dados_aluno['dados_desempenho']['notas_anteriores'] else 0.0,
                "frequenciaPresencaAtual": f"{resultado_engajamento.detalhes['percentual_presenca']:.0f}%",
                "disciplinaCritica": (
                    resultado_desempenho.detalhes['disciplinas_criticas'][0]
                    if resultado_desempenho.detalhes['disciplinas_criticas']
                    else "Nenhuma"
                )
            },
            "acaoRecomendada": {
                "playbookId": resultado_acao.detalhes['playbook_id'],
                "canal": resultado_acao.detalhes['canal'],
                "titulo": resultado_acao.detalhes['titulo'],
                "templateMensagem": resultado_acao.detalhes['template_mensagem']
            }
        }
    
    def _calcular_score_risco(
        self,
        detalhes_desempenho: Dict[str, Any],
        detalhes_engajamento: Dict[str, Any]
    ) -> int:
        """
        Calcula o score de risco de evasão (0-100).
        
        Args:
            detalhes_desempenho: Detalhes de desempenho
            detalhes_engajamento: Detalhes de engajamento
            
        Returns:
            int: Score de risco (0-100)
        """
        score = 0
        
        # Fator de queda de rendimento (até 50 pontos)
        queda = detalhes_desempenho.get('queda_rendimento', 0)
        if queda > 3:
            score += 50
        elif queda > 2:
            score += 40
        elif queda > 1:
            score += 20
        
        # Fator de frequência (até 50 pontos)
        percentual = detalhes_engajamento.get('percentual_presenca', 100)
        if percentual < 50:
            score += 50
        elif percentual < 70:
            score += 30
        elif percentual < 85:
            score += 10
        
        return min(score, 100)
    
    def _determinar_diagnostico_chave(self, detalhes_validacao: Dict[str, Any]) -> str:
        """
        Determina o diagnóstico chave baseado na validação.
        
        Args:
            detalhes_validacao: Detalhes da validação
            
        Returns:
            str: Diagnóstico chave em formato de constante
        """
        if "específica" in detalhes_validacao.get('nuances', []):
            return "DIFICULDADE_PONTUAL_EM_DISCIPLINA_CRITICA"
        elif "geral" in str(detalhes_validacao).lower():
            return "DESENGAJAMENTO_GERAL"
        else:
            return "DESEMPENHO_INSTAVEL"

