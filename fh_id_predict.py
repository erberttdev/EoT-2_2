from fh_id_data import fh_id_data
from fh_ca import campo_amostral
from fh_filter import get_filter
from config import get_supabase_client, TABLE_STATICS
import math

supabase = get_supabase_client()

def mout_filters(fh_q_dict, dict_campo_amostral, category):
    """
    Monta filtros Over/Under para uma categoria.
    
    Args:
        fh_q_dict: Dicionário com dados de query por categoria
        dict_campo_amostral: Dicionário com tamanho do campo amostral
        category: Categoria sendo processada
        
    Returns:
        tuple: (dict_filter_over, dict_filter_under)
    """
    dict_filter_over = {}
    dict_filter_under = {}
    ca_category = dict_campo_amostral.get(category, 0)
    
    # Se não houver campo amostral, retorna filtros vazios
    if ca_category == 0:
        return dict_filter_over, dict_filter_under
    
    if category == 'gols':
        atual = fh_q_dict['gols']['sum_period1']
        for i in range(1, 6):
            dict_filter_over[i] = [atual + i, get_filter(fh_q_dict, category, i)[0], 0, 0]
            dict_filter_under[i] = [atual + i, get_filter(fh_q_dict, category, i)[1], 0, 0]

    elif category == 'corners':
        atual = fh_q_dict['corners']['sum_1st_cornerkicks'][2]
        for i in range(1, 6):
            dict_filter_over[i] = [atual + i + 2, get_filter(fh_q_dict, category, i + 2)[0], 0, 0]
            dict_filter_under[i] = [atual + i + 2, get_filter(fh_q_dict, category, i + 2)[1], 0, 0]

    elif category == 'yellowcards':
        atual = fh_q_dict['yellowcards']['sum_1st_yellowcards'][2]
        for i in range(1, 6):
            dict_filter_over[i] = [atual + i, get_filter(fh_q_dict, category, i + 2)[0], 0, 0]
            dict_filter_under[i] = [atual + i, get_filter(fh_q_dict, category, i + 2)[1], 0, 0]

    return dict_filter_over, dict_filter_under

 
def mount_resp(dict_filter_over, dict_filter_under, dict_campo_amostral, category):
    """
    Calcula probabilidades e odds baseado no campo amostral.
    
    Args:
        dict_filter_over: Dicionário com filtros Over
        dict_filter_under: Dicionário com filtros Under
        dict_campo_amostral: Dicionário com tamanho do campo amostral por categoria
        category: Categoria sendo processada
        
    Returns:
        tuple: (dict_filter_over atualizado, dict_filter_under atualizado)
    """
    campo_amostral = dict_campo_amostral.get(category, 0)
    
    # Se o campo amostral for zero, não é possível calcular probabilidades
    if campo_amostral == 0:
        # Define probabilidade e odd como zero para todos os filtros
        for i in range(1, len(dict_filter_over) + 1):
            dict_filter_over[i][2] = 0  # probabilidade
            dict_filter_over[i][3] = 0   # odd
        
        for i in range(1, len(dict_filter_under) + 1):
            dict_filter_under[i][2] = 0  # probabilidade
            dict_filter_under[i][3] = 0   # odd
        
        return dict_filter_over, dict_filter_under
    
    # Calcula probabilidades e odds normalmente
    for i in range(1, len(dict_filter_over) + 1):
        prob = (dict_filter_over[i][1] * 100) / campo_amostral
        dict_filter_over[i][2] = prob
        if prob == 0:
            odd = 0
        else:
            odd = 1 / (prob / 100)
        dict_filter_over[i][3] = odd

    for i in range(1, len(dict_filter_under) + 1):
        prob = (dict_filter_under[i][1] * 100) / campo_amostral
        dict_filter_under[i][2] = prob
        if prob == 0:
            odd = 0
        else:
            odd = 1 / (prob / 100)
        dict_filter_under[i][3] = odd

    return dict_filter_over, dict_filter_under


def over_under(event_id):
    """
    Calcula previsões Over/Under para um evento.
    
    Args:
        event_id: ID do evento
        
    Returns:
        list: Lista com informações do evento e previsões
        
    Raises:
        ValueError: Se não houver dados ou estatísticas suficientes
    """
    print(f"   └─ 📥 Obtendo dados do evento...")
    event_info = fh_id_data(event_id)
    
    if event_info is None:
        raise ValueError(f"Evento {event_id}: Não foi possível obter dados do evento")
    
    try:
        dict_campo_amostral, fh_q_dict = campo_amostral(event_id)
    except ValueError as e:
        raise ValueError(f"Evento {event_id}: {str(e)}")
    
    list_resp = [event_info]
    
    print(f"   └─ ⚽ Calculando previsões de Gols...")
    category = 'gols'
    dict_filter_over, dict_filter_under = mout_filters(fh_q_dict, dict_campo_amostral, category)
    resp_over, resp_under = mount_resp(dict_filter_over, dict_filter_under, dict_campo_amostral, category)
    dict_resp = {
        'gols': [resp_over, resp_under],
    }
    list_resp.append(dict_resp)
    print(f"   └─ ✅ Previsões de Gols calculadas")

    print(f"   └─ 🚩 Calculando previsões de Escanteios...")
    category = 'corners'
    dict_filter_over, dict_filter_under = mout_filters(fh_q_dict, dict_campo_amostral, category)
    resp_over, resp_under = mount_resp(dict_filter_over, dict_filter_under, dict_campo_amostral, category)
    dict_resp = {
        'corners': [resp_over, resp_under],
    }
    list_resp.append(dict_resp)
    print(f"   └─ ✅ Previsões de Escanteios calculadas")

    print(f"   └─ 🟨 Calculando previsões de Cartões Amarelos...")
    category = 'yellowcards'
    dict_filter_over, dict_filter_under = mout_filters(fh_q_dict, dict_campo_amostral, category)
    resp_over, resp_under = mount_resp(dict_filter_over, dict_filter_under, dict_campo_amostral, category)
    dict_resp = {
        'yellowcards': [resp_over, resp_under],
    }
    list_resp.append(dict_resp)
    print(f"   └─ ✅ Previsões de Cartões Amarelos calculadas")

    return list_resp


if __name__ == "__main__":

    event_id = input("Digite o event ID: ")
    # event_id = 13472618
    over_under_resp = over_under(event_id) 
    print(over_under_resp)



