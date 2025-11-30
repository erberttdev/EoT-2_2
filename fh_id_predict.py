from fh_id_data import fh_id_data
from fh_ca import campo_amostral
from fh_filter import get_filter
import os
from supabase import create_client, Client
import math
table = 'table_statics'
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def mout_filters(fh_q_dict, dict_campo_amostral, category):
    dict_filter_over = {}
    dict_filter_under = {}
    ca_category = dict_campo_amostral[category]
    if category == 'gols':
        atual = fh_q_dict['gols']['sum_period1']
        for i in range(1,6):
            dict_filter_over[i] = [atual + i , get_filter(fh_q_dict, category, i),0,0]
            dict_filter_under[i] = [atual + i, ca_category - get_filter(fh_q_dict, category, i),0, 0]

    elif category == 'corners':
        atual = fh_q_dict['corners']['sum_1st_cornerkicks'][2]
        for i in range(1,6):
            dict_filter_over[i] = [atual + i + 2, get_filter(fh_q_dict, category, i + 2),0,0]
            dict_filter_under[i] = [atual + i + 2, ca_category - get_filter(fh_q_dict, category, i + 2),0, 0]

    elif category == 'yellowcards':
        atual = fh_q_dict['yellowcards']['sum_1st_yellowcards'][2]
        for i in range(1,6):
            dict_filter_over[i] = [atual + i , get_filter(fh_q_dict, category, i + 2),0,0]
            dict_filter_under[i] = [atual + i, ca_category - get_filter(fh_q_dict, category, i + 2),0, 0]

    return dict_filter_over, dict_filter_under

 
def mount_resp(dict_filter_over, dict_filter_under,dict_campo_amostral, category):
    for i in range(1,len(dict_filter_over) + 1):
        prob = (dict_filter_over[i][1] * 100) / dict_campo_amostral[category]
        dict_filter_over[i][2] = prob
        odd = 1/(prob/100)
        dict_filter_over[i][3] = odd

    for i in range(1,len(dict_filter_under) + 1):
        prob = (dict_filter_under[i][1] * 100) / dict_campo_amostral[category]
        dict_filter_under[i][2] = prob
        odd = 1/(prob/100)
        dict_filter_under[i][3] = odd

    return dict_filter_over, dict_filter_under


def over_under(event_id):
    dict_resp = {}
    event_info = fh_id_data(event_id)
    list_resp = [event_info]
    dict_campo_amostral, fh_q_dict = campo_amostral(event_id)
    
    category = 'gols'
    dict_filter_over, dict_filter_under = mout_filters(fh_q_dict, dict_campo_amostral, category)
    resp_over, resp_under = mount_resp(dict_filter_over, dict_filter_under,dict_campo_amostral, category)
    dict_resp = {
        'gols': [resp_over, resp_under],
    }
    list_resp.append(dict_resp)

    category = 'corners'
    dict_filter_over, dict_filter_under = mout_filters(fh_q_dict, dict_campo_amostral, category)
    resp_over, resp_under = mount_resp(dict_filter_over, dict_filter_under,dict_campo_amostral, category)
    dict_resp = {
        'corners': [resp_over, resp_under],
    }
    list_resp.append(dict_resp)

    category = 'yellowcards'
    dict_filter_over, dict_filter_under = mout_filters(fh_q_dict, dict_campo_amostral, category)
    resp_over, resp_under = mount_resp(dict_filter_over, dict_filter_under,dict_campo_amostral, category)
    dict_resp = {
        'yellowcards': [resp_over, resp_under],
    }
    list_resp.append(dict_resp)

    return list_resp


if __name__ == "__main__":

    event_id = input("Digite o event ID: ")
    # event_id = 13472618
    over_under_resp = over_under(event_id) 
    print(over_under_resp)



