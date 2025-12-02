from web_scraper import fetch_api_data
from tournament_loader import load_valid_tournament_ids
from fh_id_data import fh_id_data
import logging

logger = logging.getLogger(__name__)


def fh_live_data():
    """
    Busca partidas ao vivo que estão no intervalo (Halftime).
    
    Returns:
        list: Lista de IDs de eventos em intervalo
    """
    try:
        endpoint = "/api/v1/sport/football/events/live"
        dict_content = fetch_api_data(endpoint)
        list_events = dict_content["events"]
    except Exception as e:
        logger.error(f"Erro ao buscar partidas ao vivo: {e}")
        return []

    valid_tournament_ids = load_valid_tournament_ids()
    events_lists = []
    
    for event in list_events:
        unique_tournament = event.get('tournament', {}).get('uniqueTournament')
        if (event['status']['description'] == 'Halftime' and 
            unique_tournament and 
            str(unique_tournament.get('id')) in valid_tournament_ids):
            event_id = event['id']
            logger.info(f"Partida encontrada no intervalo: {event_id}")
            events_lists.append(event_id)


    return events_lists


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    print(fh_live_data())



