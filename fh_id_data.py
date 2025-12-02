from web_scraper import fetch_api_data
from fh_statistcs import get_FH_statistcs
import logging

logger = logging.getLogger(__name__)


def fh_id_data(even_id):
    """
    Obtém dados detalhados de um evento específico.
    
    Args:
        even_id: ID do evento no SofaScore
        
    Returns:
        dict: Dicionário com dados do evento ou None em caso de erro
    """
    print(f"   └─ 📥 Buscando dados do evento na API SofaScore...")
    try:
        endpoint = f"/api/v1/event/{even_id}"
        dict_content = fetch_api_data(endpoint)
        list_events = dict_content["event"]
        print(f"   └─ ✅ Dados do evento obtidos")
    except Exception as e:
        print(f"   └─ ❌ Erro ao buscar dados: {e}")
        logger.error(f"Erro ao buscar dados do evento {even_id}: {e}")
        return None

    events_dict = {}
    events_dict['event_id'] = list_events['id']
    events_dict['tournament_id'] = list_events['tournament']['uniqueTournament']['id']
    events_dict['id_tournament'] = list_events['tournament']['uniqueTournament']['name']
    events_dict['home_name'] = list_events['homeTeam']['name']
    events_dict['away_name'] = list_events['awayTeam']['name']
    events_dict['home_score'] = list_events['homeScore']['period1']
    events_dict['awayScore'] = list_events['awayScore']['period1']
    
    print(f"   └─ 📋 Partida: {events_dict['home_name']} {events_dict['home_score']}-{events_dict['awayScore']} {events_dict['away_name']}")
    print(f"   └─ 🏆 Torneio: {events_dict['id_tournament']}")

    print(f"   └─ 📊 Buscando estatísticas do primeiro tempo...")
    try:
        events_dict['home_statistics'], events_dict['away_statistics'] = get_FH_statistcs(events_dict['event_id'])
        print(f"   └─ ✅ Estatísticas obtidas com sucesso")
    except Exception as e:
        print(f"   └─ ⚠️  Sem estatísticas disponíveis: {e}")
        logger.warning(f'Sem estatisticas para {events_dict["event_id"]}: {e}')
        events_dict = None
        
    return events_dict



if __name__ == "__main__":

    event_id = input("Digite o event ID: ")
    print(fh_id_data(event_id))



