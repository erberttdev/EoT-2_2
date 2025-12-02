
from fh_live_data import fh_live_data
from predict_fh import processar_e_enviar_evento
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logger = logging.getLogger(__name__)


def main_task():
    """
    Busca partidas ao vivo e processa cada uma individualmente,
    enviando uma mensagem por evento.
    """
    list_ids_live = fh_live_data()
    # list_ids_live = [14109730, 14109726, 13472608]  # Para testes
    
    if len(list_ids_live) > 0:
        logger.info(f'Encontradas {len(list_ids_live)} partidas ao vivo')
        
        # Processa cada evento individualmente
        for event_id in list_ids_live:
            processar_e_enviar_evento(event_id)
        
        logger.info(f'Processamento concluído para {len(list_ids_live)} eventos')
    else:
        logger.info('Nenhuma partida ao vivo encontrada no momento.')


if __name__ == "__main__":
    # Configurar logging para APScheduler
    logging.basicConfig(level=logging.INFO)

    # Criar scheduler
    scheduler = BlockingScheduler()

    # Agendar a tarefa para executar a cada 10 minutos
    scheduler.add_job(main_task, 'interval', minutes=10)

    # Executar a tarefa imediatamente na primeira vez
    main_task()

    # Iniciar o scheduler
    scheduler.start()
