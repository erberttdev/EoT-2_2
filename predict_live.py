from fh_id_data import fh_id_data
from fh_ca import campo_amostral
from fh_filter import get_filter
from fh_live_data import fh_live_data
from fh_id_predict import over_under
import os
from supabase import create_client, Client
import math
table = 'table_statics'
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def filter_min(over_under_resp, min_percent=70, min_odd=1.2):

    dict_gols_over = over_under_resp[1]['gols'][0]
    dict_gols_under = over_under_resp[1]['gols'][1]
    dict_info = over_under_resp[0]
    list_gols_over_resp = []
    list_gols_under_resp = []
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

    if len(list_gols_over_resp) + len(list_gols_under_resp) > 0:
        dict_resposta['info'] = dict_info


    return dict_resposta

def resposts_live(list_ids_live):
    list_resposts = []
    for id_live in list_ids_live:
        print(f'Processing live id: {id_live}')
        over_under_resp = over_under(id_live) 
        list_resposts.append(filter_min(over_under_resp))

    return list_resposts

if __name__ == "__main__":
    
    list_ids_live = fh_live_data()
    # list_ids_live = [13981543,14064430]
    resposts_live(list_ids_live)