from web_scraper import fetch_api_data
import logging

logger = logging.getLogger(__name__)


def get_statistc_values(fh_statistic, s_key):
    """
    Extrai valores de estatísticas de um grupo de estatísticas.
    
    Args:
        fh_statistic: Lista de grupos de estatísticas
        s_key: Chave da estatística a buscar
        
    Returns:
        tuple: (valor_casa, valor_visitante) ou (0, 0) se não encontrado
    """
    for group in fh_statistic:
        for statistic in group.get('statisticsItems', []):
            if statistic.get('key') == s_key:
                return (statistic.get('homeValue', 0), statistic.get('awayValue', 0))
    return (0, 0)


def get_FH_statistcs(event_id):
    """
    Obtém estatísticas do primeiro tempo de um evento.
    
    Args:
        event_id: ID do evento no SofaScore
        
    Returns:
        tuple: (home_statistics_dict, away_statistics_dict)
    """
    try:
        endpoint = f"/api/v1/event/{event_id}/statistics"
        dict_content = fetch_api_data(endpoint)
        list_statistcs = dict_content["statistics"]
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas do evento {event_id}: {e}")
        raise

    home_statics_dict = {}
    away_statics_dict = {}
    
    if len(list_statistcs) < 2:
        logger.warning(f"Estatísticas do primeiro tempo não encontradas para evento {event_id}")
        return home_statics_dict, away_statics_dict
    
    fh_statistic = list_statistcs[1].get('groups', [])
    print(f"      └─ 📈 Processando {len(fh_statistic)} grupos de estatísticas...")
    
    # Mapeamento de chaves de estatísticas
    stats_mapping = {
        'Ball possession': 'ballPossession',
        'Expected goals': 'expectedGoals',
        'Total shots': 'totalShotsOnGoal',
        'Shots on target': 'shotsOnGoal',
        'Shots inside box': 'totalShotsInsideBox',
        'Final third entries': 'finalThirdEntries',
        'cornerKicks': 'cornerKicks',
        'fouls': 'fouls',
        'yellowCards': 'yellowCards'
    }
    
    for stat_name, stat_key in stats_mapping.items():
        home_val, away_val = get_statistc_values(fh_statistic, stat_key)
        home_statics_dict[stat_name] = home_val
        away_statics_dict[stat_name] = away_val

    return home_statics_dict, away_statics_dict



if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    event_id = input("Digite o event ID: ")
    print(get_FH_statistcs(event_id))
