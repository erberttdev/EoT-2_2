
from fh_day_data import fh_day_data
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
    
    event_data_txt = input("Digite a data do evento (dd-mm-aaaa): ").strip()
    event_data_lst = event_data_txt.split('-')
    event_data = f'{event_data_lst[2]}-{event_data_lst[1]}-{event_data_lst[0]}'
    list_ids_live = fh_day_data(event_data)


    if len(list_ids_live) > 0:
        list_resposts_live = resposts_live(list_ids_live)
        mensagem = formatar_resultado(list_resposts_live)
        enviar_mensagem_telegram(mensagem)
    else:
        print('***** SEM PARTIDAS ENCONTRADAS *****.')


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
