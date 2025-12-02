
from fh_live_data import fh_live_data
from send_telegram import enviar_mensagem_telegram, formatar_resultado
from predict_fh import resposts_live
import os
from supabase import create_client, Client
import math
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
table = 'table_statics'
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)



def main_task():
    
    list_ids_live_input = input('Digite os IDs das partidas ao vivo separados por vírgula: ').split(',')
    list_ids_live = [int(list_id.strip()) for list_id in list_ids_live_input]
    if len(list_ids_live) > 0:
        list_resposts_live = resposts_live(list_ids_live)
        mensagem = formatar_resultado(list_resposts_live)
        enviar_mensagem_telegram(mensagem)
    else:
        print('***** NENHUMA PARTIDA ENCONTRADA *****.')


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
