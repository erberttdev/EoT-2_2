from fh_id_data import fh_id_data
import os
from supabase import create_client, Client
table = 'table_statics'
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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
    fh_sum_data = {}
    fh_sum_data['sum_period1'] = fh_event_data['home_score'] +  fh_event_data['awayScore']
    fh_sum_data['sum_expected_goals_1st'] = fh_event_data['home_statistics']['Expected goals'] +  fh_event_data['away_statistics']['Expected goals'] 
    fh_sum_data['sum_1st_totalshotsongoal'] = fh_event_data['home_statistics']['Total shots'] +  fh_event_data['away_statistics']['Total shots'] 
    fh_sum_data['sum_1st_shotsongoal'] = fh_event_data['home_statistics']['Shots on target'] +  fh_event_data['away_statistics']['Shots on target'] 
    fh_sum_data['sum_1st_totalshotsinsidebox'] = fh_event_data['home_statistics']['Shots inside box'] +  fh_event_data['away_statistics']['Shots inside box'] 
    fh_sum_data['sum_1st_finalthirdentries'] = fh_event_data['home_statistics']['Final third entries'] +  fh_event_data['away_statistics']['Final third entries'] 
    fh_sum_data['sum_1st_cornerkicks'] = fh_event_data['home_statistics']['cornerKicks'] +  fh_event_data['away_statistics']['cornerKicks'] 
    fh_sum_data['sum_1st_freekicks'] = fh_event_data['home_statistics']['fouls'] +  fh_event_data['away_statistics']['fouls'] 
    fh_sum_data['sum_1st_yellowcards'] = fh_event_data['home_statistics']['yellowCards'] +  fh_event_data['away_statistics']['yellowCards'] 
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
        supabase.table(table)
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
        supabase.table(table)
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
        supabase.table(table)
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
    while ca_temp < 100 and i <=4:
        fh_q_data = apply_tolerance(fh_sum_data,threshold,i)
        ca_temp = get_campo_amostral(fh_q_data, fh_sum_data, category)
        # print(f'Tolerancia {i} ', ca_temp)
        i += 1

    ca_value = ca_temp
    return ca_value, fh_q_data

def get_fh_sum(event_id):
    fh_event_data = fh_id_data(event_id)
    fh_sum_data = sum_data(fh_event_data)

    return fh_sum_data, fh_event_data

def get_ca_q_data(fh_sum_data):
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
    fh_sum_data, fh_event_data  = get_fh_sum(event_id)
    dict_campo_amostral, fh_q_dict = get_ca_q_data(fh_sum_data)

    
    return dict_campo_amostral, fh_q_dict





if __name__ == "__main__":

    event_id = input("Digite o event ID: ")
    print(campo_amostral(event_id)[0])
