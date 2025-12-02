
from predict_fh import processar_e_enviar_evento
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logger = logging.getLogger(__name__)


def main_task():
    """
    Processa IDs de eventos fornecidos manualmente, um por um,
    enviando uma mensagem por evento.
    """
    list_ids_live_input = input('Digite os IDs das partidas separados por vírgula: ').split(',')
    list_ids_live = [int(list_id.strip()) for list_id in list_ids_live_input if list_id.strip().isdigit()]
    
    if len(list_ids_live) > 0:
        logger.info(f'Processando {len(list_ids_live)} eventos fornecidos')
        
        # Processa cada evento individualmente
        for event_id in list_ids_live:
            processar_e_enviar_evento(event_id)
        
        logger.info(f'Processamento concluído para {len(list_ids_live)} eventos')
    else:
        logger.warning('Nenhum ID válido fornecido.')


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
