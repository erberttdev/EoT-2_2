from fh_id_data import fh_id_data
from config import get_supabase_client, TABLE_STATICS

supabase = get_supabase_client()

threshold = [
    {
 'sum_expected_goals_1st': (0.25, 0.25),
 'sum_1st_totalshotsongoal': (2, 2) ,
 'sum_1st_shotsongoal': (1, 1),
 'sum_1st_totalshotsinsidebox': (1, 1),
 'sum_1st_finalthirdentries': (15, 15),
 'sum_1st_cornerkicks': (2, 2),
 'sum_1st_freekicks': (2, 2),
 'sum_1st_yellowcards': (1, 1)
    } , 
        {
 'sum_expected_goals_1st': (0.5, 0.5),
 'sum_1st_totalshotsongoal': (3, 3) ,
 'sum_1st_shotsongoal': (2, 2),
 'sum_1st_totalshotsinsidebox': (2, 2),
 'sum_1st_finalthirdentries': (25, 25),
 'sum_1st_cornerkicks': (3, 3),
 'sum_1st_freekicks': (3, 3),
 'sum_1st_yellowcards': (2, 2)
    } , 
            {
 'sum_expected_goals_1st': (0.5, 0.5),
 'sum_1st_totalshotsongoal': (3, 3) ,
 'sum_1st_shotsongoal': (3, 3),
 'sum_1st_totalshotsinsidebox': (3, 3),
 'sum_1st_finalthirdentries': (30, 30),
 'sum_1st_cornerkicks': (3, 3),
 'sum_1st_freekicks': (3, 3),
 'sum_1st_yellowcards': (2, 2)
    } , 
    {
 'sum_expected_goals_1st': (1.0, 1.0),
 'sum_1st_totalshotsongoal': (5, 5) ,
 'sum_1st_shotsongoal': (5, 5),
 'sum_1st_totalshotsinsidebox': (5, 5),
 'sum_1st_finalthirdentries': (50, 50),
 'sum_1st_cornerkicks': (5, 5),
 'sum_1st_freekicks': (5, 5),
 'sum_1st_yellowcards': (4, 4)
    } , 
    
 ]

def sum_data(fh_event_data):
    """
    Calcula a soma das estatísticas do primeiro tempo.
    
    Args:
        fh_event_data: Dicionário com dados do evento e estatísticas
        
    Returns:
        dict: Dicionário com somas das estatísticas
        
    Raises:
        ValueError: Se fh_event_data for None ou não tiver estatísticas necessárias
    """
    if fh_event_data is None:
        raise ValueError("Dados do evento não disponíveis (None)")
    
    if 'home_statistics' not in fh_event_data or 'away_statistics' not in fh_event_data:
        raise ValueError("Estatísticas do primeiro tempo não disponíveis para este evento")
    
    home_stats = fh_event_data['home_statistics']
    away_stats = fh_event_data['away_statistics']
    
    # Função auxiliar para obter valor seguro de estatística
    def get_stat(stat_key, default=0):
        return home_stats.get(stat_key, default) + away_stats.get(stat_key, default)
    
    fh_sum_data = {}
    fh_sum_data['sum_period1'] = fh_event_data.get('home_score', 0) + fh_event_data.get('awayScore', 0)
    fh_sum_data['sum_expected_goals_1st'] = get_stat('Expected goals', 0)
    fh_sum_data['sum_1st_totalshotsongoal'] = get_stat('Total shots', 0)
    fh_sum_data['sum_1st_shotsongoal'] = get_stat('Shots on target', 0)
    fh_sum_data['sum_1st_totalshotsinsidebox'] = get_stat('Shots inside box', 0)
    fh_sum_data['sum_1st_finalthirdentries'] = get_stat('Final third entries', 0)
    fh_sum_data['sum_1st_cornerkicks'] = get_stat('cornerKicks', 0)
    fh_sum_data['sum_1st_freekicks'] = get_stat('fouls', 0)
    fh_sum_data['sum_1st_yellowcards'] = get_stat('yellowCards', 0)
    
    return fh_sum_data


def apply_tolerance(fh_sum_data,threshold,relax):
    fh_q_data = {}
    fh_q_data['sum_period1'] = fh_sum_data['sum_period1']
    fh_q_data['sum_expected_goals_1st'] = (fh_sum_data['sum_expected_goals_1st'] - threshold[relax]['sum_expected_goals_1st'][0] , fh_sum_data['sum_expected_goals_1st'] + threshold[relax]['sum_expected_goals_1st'][1] )
    fh_q_data['sum_1st_totalshotsongoal'] = (fh_sum_data['sum_1st_totalshotsongoal'] - threshold[relax]['sum_1st_totalshotsongoal'][0] , fh_sum_data['sum_1st_totalshotsongoal'] + threshold[relax]['sum_1st_totalshotsongoal'][1] )
    fh_q_data['sum_1st_shotsongoal'] = (fh_sum_data['sum_1st_shotsongoal'] - threshold[relax]['sum_1st_shotsongoal'][0] , fh_sum_data['sum_1st_shotsongoal'] + threshold[relax]['sum_1st_shotsongoal'][1] )
    fh_q_data['sum_1st_totalshotsinsidebox'] = (fh_sum_data['sum_1st_totalshotsinsidebox'] - threshold[relax]['sum_1st_totalshotsinsidebox'][0] , fh_sum_data['sum_1st_totalshotsinsidebox'] + threshold[relax]['sum_1st_totalshotsinsidebox'][1] )
    fh_q_data['sum_1st_finalthirdentries'] = (fh_sum_data['sum_1st_finalthirdentries'] - threshold[relax]['sum_1st_finalthirdentries'][0] , fh_sum_data['sum_1st_finalthirdentries'] + threshold[relax]['sum_1st_finalthirdentries'][1] )
    fh_q_data['sum_1st_cornerkicks'] = (fh_sum_data['sum_1st_cornerkicks'] - threshold[relax]['sum_1st_cornerkicks'][0] , fh_sum_data['sum_1st_cornerkicks'] + threshold[relax]['sum_1st_cornerkicks'][1], fh_sum_data['sum_1st_cornerkicks'] )
    fh_q_data['sum_1st_freekicks'] = (fh_sum_data['sum_1st_freekicks'] - threshold[relax]['sum_1st_freekicks'][0] , fh_sum_data['sum_1st_freekicks'] + threshold[relax]['sum_1st_freekicks'][1] )
    fh_q_data['sum_1st_yellowcards'] = (fh_sum_data['sum_1st_yellowcards'] - threshold[relax]['sum_1st_yellowcards'][0] , fh_sum_data['sum_1st_yellowcards'] + threshold[relax]['sum_1st_yellowcards'][1], fh_sum_data['sum_1st_yellowcards'] )

    return fh_q_data

def get_campo_amostral(fh_q_data, fh_sum_data, category):

    if category == 'corners':
        response = (
        supabase.table(TABLE_STATICS)
        .select("*")
        .eq('sum_period1', fh_sum_data['sum_period1'])
        .eq('sum_1st_cornerkicks', fh_sum_data['sum_1st_cornerkicks'])
        .gte("sum_1st_totalshotsongoal", fh_q_data['sum_1st_totalshotsongoal'][0]).lte("sum_1st_totalshotsongoal", fh_q_data['sum_1st_totalshotsongoal'][1])
        # .gte("sum_1st_shotsongoal", fh_q_data['sum_1st_shotsongoal'][0]).lte("sum_1st_shotsongoal", fh_q_data['sum_1st_shotsongoal'][1])
        # .gte("sum_1st_finalthirdentries", fh_q_data['sum_1st_finalthirdentries'][0]).lte("sum_1st_finalthirdentries", fh_q_data['sum_1st_finalthirdentries'][1])
        .execute()
    )
    elif category == 'gols':
        response = (
        supabase.table(TABLE_STATICS)
        .select("*")
        .eq('sum_period1', fh_sum_data['sum_period1'])
        .gte("sum_expected_goals_1st", fh_q_data['sum_expected_goals_1st'][0]).lte("sum_expected_goals_1st", fh_q_data['sum_expected_goals_1st'][1])
        .gte("sum_1st_shotsongoal", fh_q_data['sum_1st_shotsongoal'][0]).lte("sum_1st_shotsongoal", fh_q_data['sum_1st_shotsongoal'][1])
        .gte("sum_1st_totalshotsinsidebox", fh_q_data['sum_1st_totalshotsinsidebox'][0]).lte("sum_1st_totalshotsinsidebox", fh_q_data['sum_1st_totalshotsinsidebox'][1])
        .gte("sum_1st_finalthirdentries", fh_q_data['sum_1st_finalthirdentries'][0]).lte("sum_1st_finalthirdentries", fh_q_data['sum_1st_finalthirdentries'][1])
        
        .execute()
        )

    elif category == 'yellowcards':
        
        response = (
        supabase.table(TABLE_STATICS)
        .select("*")
        .eq('sum_1st_yellowcards', fh_sum_data['sum_1st_yellowcards'])
        .gte("sum_1st_freekicks", fh_q_data['sum_1st_freekicks'][0]).lte("sum_1st_freekicks", fh_q_data['sum_1st_freekicks'][1])
        .gte("sum_1st_finalthirdentries", fh_q_data['sum_1st_finalthirdentries'][0]).lte("sum_1st_finalthirdentries", fh_q_data['sum_1st_finalthirdentries'][1])
        
        .execute()
    )

    return len(response.data)


def c_amostral(fh_sum_data, category):
    ca_temp = 0
    i = 0
    while ca_temp < 100 and i < 4:
        fh_q_data = apply_tolerance(fh_sum_data,threshold,i)
        ca_temp = get_campo_amostral(fh_q_data, fh_sum_data, category)
        # print(f'Tolerancia {i} ', ca_temp)
        i += 1

    ca_value = ca_temp
    return ca_value, fh_q_data

def get_fh_sum(event_id):
    """
    Obtém dados do evento e calcula somas das estatísticas.
    
    Args:
        event_id: ID do evento
        
    Returns:
        tuple: (fh_sum_data, fh_event_data)
        
    Raises:
        ValueError: Se não houver dados ou estatísticas do evento
    """
    print(f"   └─ 🔢 Calculando somas das estatísticas do primeiro tempo...")
    fh_event_data = fh_id_data(event_id)
    
    if fh_event_data is None:
        raise ValueError(f"Evento {event_id}: Dados do evento não disponíveis")
    
    try:
        fh_sum_data = sum_data(fh_event_data)
        print(f"   └─ ✅ Somas calculadas: {fh_sum_data.get('sum_period1', 0)} gols, {fh_sum_data.get('sum_1st_cornerkicks', 0)} corners")
    except ValueError as e:
        raise ValueError(f"Evento {event_id}: {str(e)}")
    
    return fh_sum_data, fh_event_data

def get_ca_q_data(fh_sum_data):
    """
    Calcula campo amostral e dados de query para todas as categorias.
    
    Args:
        fh_sum_data: Dados somados das estatísticas
        
    Returns:
        tuple: (dict_campo_amostral, fh_q_dict)
    """
    ca_gols, fh_q_gols = c_amostral(fh_sum_data, 'gols')
    ca_corners, fh_q_corners = c_amostral(fh_sum_data, 'corners')
    ca_yellowcards, fh_q_yellowcards = c_amostral(fh_sum_data, 'yellowcards')

    dict_campo_amostral = {
        'gols': ca_gols,
        'corners': ca_corners,
        'yellowcards': ca_yellowcards
    }

    fh_q_dict = {
        'gols': fh_q_gols,
        'corners': fh_q_corners,
        'yellowcards': fh_q_yellowcards
    }

    return dict_campo_amostral, fh_q_dict



def campo_amostral(event_id):
    """
    Calcula campo amostral para um evento.
    
    Args:
        event_id: ID do evento
        
    Returns:
        tuple: (dict_campo_amostral, fh_q_dict)
        
    Raises:
        ValueError: Se não houver dados ou estatísticas suficientes
    """
    print(f"   └─ 🎯 Calculando campo amostral...")
    try:
        fh_sum_data, fh_event_data = get_fh_sum(event_id)
        dict_campo_amostral, fh_q_dict = get_ca_q_data(fh_sum_data)
        
        print(f"   └─ 📊 Campo amostral: Gols={dict_campo_amostral.get('gols', 0)}, "
              f"Corners={dict_campo_amostral.get('corners', 0)}, "
              f"Cartões={dict_campo_amostral.get('yellowcards', 0)}")
        
        return dict_campo_amostral, fh_q_dict
    except ValueError as e:
        # Re-raise ValueError para que seja capturado pelo chamador
        raise
    except Exception as e:
        raise ValueError(f"Erro ao calcular campo amostral para evento {event_id}: {str(e)}")





if __name__ == "__main__":

    event_id = input("Digite o event ID: ")
    print(campo_amostral(event_id)[0])
