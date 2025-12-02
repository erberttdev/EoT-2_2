"""
Módulo para salvar previsões em arquivo CSV.
"""
import csv
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Nome do arquivo CSV
CSV_FILENAME = 'predictions.csv'


def save_predictions_to_csv(resultado_filtrado, event_info):
    """
    Salva as previsões filtradas em um arquivo CSV.
    
    Cada previsão é salva como uma linha contendo:
    - event_id: ID do evento
    - tournament_id: ID do torneio
    - categoria: Categoria da previsão (gols, escanteios, cartão amarelo)
    - tipo_previsao: Tipo de previsão (Over ou Under)
    - target: Valor alvo da previsão
    - prob: Probabilidade da previsão (em %)
    - resultado: Campo para preencher posteriormente (GREEN ou RED) - inicialmente vazio
    - version: Versão da previsão (padrão: V1)
    
    Args:
        resultado_filtrado: Dicionário com previsões filtradas
        event_info: Dicionário com informações do evento (deve conter event_id e tournament_id)
    """
    if not resultado_filtrado or 'info' not in resultado_filtrado:
        logger.debug('Nenhuma previsão para salvar')
        return
    
    event_id = event_info.get('event_id')
    tournament_id = event_info.get('tournament_id')
    
    
    if not event_id:
        logger.warning('Evento sem event_id, não é possível salvar previsões')
        return
    
    # Mapeamento de categorias para nomes legíveis
    categoria_map = {
        'gols': 'gols',
        'corners': 'escanteios',
        'yellowcards': 'cartão amarelo'
    }
    
    # Verificar se o arquivo existe para determinar se precisa escrever o cabeçalho
    file_exists = os.path.exists(CSV_FILENAME)
    
    try:
        with open(CSV_FILENAME, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['event_id', 'tournament_id', 'categoria', 'tipo_previsao', 'target', 'prob', 'resultado', 'version']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Escrever cabeçalho apenas se o arquivo não existir
            if not file_exists:
                writer.writeheader()
            
            # Processar cada tipo de previsão
            previsoes_salvas = 0
            
            # Gols Over
            if 'gols_over' in resultado_filtrado:
                for previsao in resultado_filtrado['gols_over']:
                    # previsao é uma lista: [target, quantidade, probabilidade, odd]
                    target = previsao[0]
                    prob = int(previsao[2]) if previsao[2] is not None else 0
                    writer.writerow({
                        'event_id': event_id,
                        'tournament_id': tournament_id if tournament_id else '',
                        'categoria': categoria_map.get('gols', 'gols'),
                        'tipo_previsao': 'Over',
                        'target': target,
                        'prob': prob,
                        'resultado': '',
                        'version': 'V1'
                    })
                    previsoes_salvas += 1
            
            # Gols Under
            if 'gols_under' in resultado_filtrado:
                for previsao in resultado_filtrado['gols_under']:
                    target = previsao[0]
                    prob = int(previsao[2]) if previsao[2] is not None else 0
                    writer.writerow({
                        'event_id': event_id,
                        'tournament_id': tournament_id if tournament_id else '',
                        'categoria': categoria_map.get('gols', 'gols'),
                        'tipo_previsao': 'Under',
                        'target': target,
                        'prob': prob,
                        'resultado': '',
                        'version': 'V1'
                    })
                    previsoes_salvas += 1
            
            # Escanteios Over
            if 'corners_over' in resultado_filtrado:
                for previsao in resultado_filtrado['corners_over']:
                    target = previsao[0]
                    prob = int(previsao[2]) if previsao[2] is not None else 0
                    writer.writerow({
                        'event_id': event_id,
                        'tournament_id': tournament_id if tournament_id else '',
                        'categoria': categoria_map.get('corners', 'escanteios'),
                        'tipo_previsao': 'Over',
                        'target': target,
                        'prob': prob,
                        'resultado': '',
                        'version': 'V1'
                    })
                    previsoes_salvas += 1
            
            # Escanteios Under
            if 'corners_under' in resultado_filtrado:
                for previsao in resultado_filtrado['corners_under']:
                    target = previsao[0]
                    prob = int(previsao[2]) if previsao[2] is not None else 0
                    writer.writerow({
                        'event_id': event_id,
                        'tournament_id': tournament_id if tournament_id else '',
                        'categoria': categoria_map.get('corners', 'escanteios'),
                        'tipo_previsao': 'Under',
                        'target': target,
                        'prob': prob,
                        'resultado': '',
                        'version': 'V1'
                    })
                    previsoes_salvas += 1
            
            # Cartões Amarelos Over
            if 'yellowcards_over' in resultado_filtrado:
                for previsao in resultado_filtrado['yellowcards_over']:
                    target = previsao[0]
                    prob = int(previsao[2]) if previsao[2] is not None else 0
                    writer.writerow({
                        'event_id': event_id,
                        'tournament_id': tournament_id if tournament_id else '',
                        'categoria': categoria_map.get('yellowcards', 'cartão amarelo'),
                        'tipo_previsao': 'Over',
                        'target': target,
                        'prob': prob,
                        'resultado': '',
                        'version': 'V1'
                    })
                    previsoes_salvas += 1
            
            # Cartões Amarelos Under
            if 'yellowcards_under' in resultado_filtrado:
                for previsao in resultado_filtrado['yellowcards_under']:
                    target = previsao[0]
                    prob = int(previsao[2]) if previsao[2] is not None else 0
                    writer.writerow({
                        'event_id': event_id,
                        'tournament_id': tournament_id if tournament_id else '',
                        'categoria': categoria_map.get('yellowcards', 'cartão amarelo'),
                        'tipo_previsao': 'Under',
                        'target': target,
                        'prob': prob,
                        'resultado': '',
                        'version': 'V1'
                    })
                    previsoes_salvas += 1
        
        if previsoes_salvas > 0:
            logger.info(f'✅ {previsoes_salvas} previsões salvas no arquivo {CSV_FILENAME}')
        else:
            logger.debug('Nenhuma previsão foi salva')
            
    except Exception as e:
        logger.error(f'Erro ao salvar previsões no CSV: {e}', exc_info=True)

