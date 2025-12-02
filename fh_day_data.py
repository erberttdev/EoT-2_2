from web_scraper import fetch_api_data
from tournament_loader import load_valid_tournament_ids
import logging

logger = logging.getLogger(__name__)


def fh_day_data(event_data):
    """
    Busca partidas agendadas para uma data específica.
    
    Args:
        event_data: Data no formato 'YYYY-MM-DD'
        
    Returns:
        list: Lista de IDs de eventos agendados para a data
    """
    try:
        endpoint = f"/api/v1/sport/football/scheduled-events/{event_data}"
        dict_content = fetch_api_data(endpoint)
        list_events = dict_content["events"]
    except Exception as e:
        logger.error(f"Erro ao buscar partidas do dia {event_data}: {e}")
        return []

    valid_tournament_ids = load_valid_tournament_ids()
    events_lists = []
    
    for event in list_events:
        tournament_id = str(event['tournament']['uniqueTournament']['id'])
        if tournament_id in valid_tournament_ids:
            event_id = event['id']
            events_lists.append(event_id)
    
    logger.info(f'✅ Total de {len(events_lists)} partidas no dia {event_data}')
    return events_lists


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    event_data_txt = input("Digite a data do evento (dd-mm-aaaa): ").strip()
    event_data_lst = event_data_txt.split('-')
    event_data = f'{event_data_lst[2]}-{event_data_lst[1]}-{event_data_lst[0]}'

    print(fh_day_data(event_data))