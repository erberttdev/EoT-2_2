
from fh_day_data import fh_day_data
from predict_fh import processar_e_enviar_evento
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logger = logging.getLogger(__name__)


def main_task():
    """
    Busca partidas de uma data específica e processa cada uma individualmente,
    enviando uma mensagem por evento.
    """
    event_data_txt = input("Digite a data do evento (dd-mm-aaaa): ").strip()
    event_data_lst = event_data_txt.split('-')
    event_data = f'{event_data_lst[2]}-{event_data_lst[1]}-{event_data_lst[0]}'
    
    list_ids_live = fh_day_data(event_data)

    if len(list_ids_live) > 0:
        logger.info(f'Encontradas {len(list_ids_live)} partidas para o dia {event_data}')
        
        # Processa cada evento individualmente
        for event_id in list_ids_live:
            processar_e_enviar_evento(event_id)
        
        logger.info(f'Processamento concluído para {len(list_ids_live)} eventos')
    else:
        logger.info(f'Nenhuma partida encontrada para o dia {event_data}.')


if __name__ == "__main__":
    # # Configurar logging para APScheduler
    # logging.basicConfig(level=logging.INFO)

    # # Criar scheduler
    # scheduler = BlockingScheduler()

    # # Agendar a tarefa para executar a cada 10 minutos
    # scheduler.add_job(main_task, 'interval', minutes=10)

    # Executar a tarefa imediatamente na primeira vez
    main_task()

    # # Iniciar o scheduler
    # scheduler.start()
