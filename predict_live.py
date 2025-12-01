from fh_id_data import fh_id_data
from fh_ca import campo_amostral
from fh_filter import get_filter
from fh_live_data import fh_live_data
from fh_id_predict import over_under
from send_telegram import enviar_mensagem_telegram, formatar_resultado
import os
from supabase import create_client, Client
import math
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
table = 'table_statics'
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def filter_min(over_under_resp, min_percent=70, min_odd=1.2):

    dict_gols_over = over_under_resp[1]['gols'][0]
    dict_gols_under = over_under_resp[1]['gols'][1]
    dict_corners_over = over_under_resp[2]['corners'][0]
    dict_corners_under = over_under_resp[2]['corners'][1]
    dict_yellow_cards_over = over_under_resp[3]['yellowcards'][0]
    dict_yellow_cards_under = over_under_resp[3]['yellowcards'][1]
    dict_info = over_under_resp[0]
    list_gols_over_resp = []
    list_gols_under_resp = []
    list_corners_over_resp = []
    list_corners_under_resp = []
    list_yellow_cards_over_resp = []
    list_yellow_cards_under_resp = []
    dict_resposta = {}
    for key, value in dict_gols_over.items():
        if (value[2] >= min_percent) and (value[3] >= min_odd):
            list_gols_over_resp.append(dict_gols_over[key])


    for key, value in dict_gols_under.items():
        if (value[2] >= min_percent) and (value[3] >= min_odd):
            list_gols_under_resp.append(dict_gols_under[key])


    if len(list_gols_over_resp) > 0:
        dict_resposta['gols_over'] = list_gols_over_resp
    if len(list_gols_under_resp) > 0:
        dict_resposta['gols_under'] = list_gols_under_resp

    if len(list_corners_over_resp) > 0:
        dict_resposta['corners_over'] = list_corners_over_resp
    if len(list_corners_under_resp) > 0:
        dict_resposta['corners_under'] = list_corners_under_resp
    
    if len(list_yellow_cards_over_resp) > 0:
        dict_resposta['yellowcards_over'] = list_yellow_cards_over_resp
    if len(list_yellow_cards_under_resp) > 0:
        dict_resposta['yellowcards_under'] = list_yellow_cards_under_resp
    

    if len(list_gols_over_resp) + len(list_gols_under_resp) + len(list_corners_over_resp) + len(list_corners_under_resp) + len(list_yellow_cards_over_resp) + len(list_yellow_cards_under_resp)> 0:
        dict_resposta['info'] = dict_info
        


    return dict_resposta


def resposts_live(list_ids_live):
    list_resposts = []
    for id_live in list_ids_live:
        print(f'Processing live id: {id_live}')
        over_under_resp = over_under(id_live) 
        list_resposts.append(filter_min(over_under_resp))

    return list_resposts

def main_task():
    # list_ids_live = fh_live_data()
    list_ids_live = [14131963, 13472611,13472608]
    if len(list_ids_live) > 0:
        list_resposts_live = resposts_live(list_ids_live)
        mensagem = formatar_resultado(list_resposts_live)
        enviar_mensagem_telegram(mensagem)
    else:
        print('No live matches found.')


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
