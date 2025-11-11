#!/usr/bin/env python3
"""
Script principal: analisar_aluno.py

Este é o ponto de entrada do sistema VeloEdu Challenge.
Ele recebe um ID de aluno e um arquivo CSV com dados acadêmicos,
e retorna uma análise completa em formato JSON.

#!Uso:
   python analisar_aluno.py --arquivo historico_academico.csv --id alu_101
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from __init__ import CoordenadorAnalise

def main():
    """
    Função principal que orquestra a execução do programa.
    """
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(
        description='Analisa dados acadêmicos de um aluno usando um sistema multiagente'
    )
    
    parser.add_argument(
        '--arquivo',
        required=True,
        help='Caminho para o arquivo CSV com histórico acadêmico'
    )
    
    parser.add_argument(
        '--id',
        required=True,
        help='ID do aluno a ser analisado'
    )
    
    # Faz o parse dos argumentos
    args = parser.parse_args()
    
    # Valida se o arquivo existe
    if not os.path.exists(args.arquivo):
        print(f"Erro: Arquivo '{args.arquivo}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Cria uma instância do coordenador
        coordenador = CoordenadorAnalise(args.arquivo)
        
        # Executa a análise
        resultado = coordenador.analisar({'id_aluno': args.id})
        
        # Verifica se a análise foi bem-sucedida
        if resultado.status == "erro":
            print(f"Erro na análise: {resultado.resultado}", file=sys.stderr)
            sys.exit(1)
        
        # Imprime o JSON final
        json_final = resultado.detalhes
        print(json.dumps(json_final, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Erro ao executar análise: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

