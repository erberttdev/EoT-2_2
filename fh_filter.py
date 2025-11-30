from fh_id_data import fh_id_data
from fh_ca import campo_amostral
import os
from supabase import create_client, Client
import math
table = 'table_statics'
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_over_filter(fh_q_dict, category, soma):
    if category == 'corners':
            atual = fh_q_dict[category]['sum_1st_cornerkicks'][2] 
            target = atual + soma
            response = (
            supabase.table(table)
            .select("*") 
            .eq('sum_period1', fh_q_dict[category]['sum_period1'])
            .eq('sum_1st_cornerkicks', fh_q_dict[category]['sum_1st_cornerkicks'][2])
            .gt('sum_all_cornerkicks', target)
            .gte("sum_1st_totalshotsongoal", fh_q_dict[category]['sum_1st_totalshotsongoal'][0]).lte("sum_1st_totalshotsongoal", fh_q_dict[category]['sum_1st_totalshotsongoal'][1])
            
            .execute()
        )
    elif category == 'gols':
        atual = fh_q_dict[category]['sum_period1']
        target = atual + soma
        response = (
        supabase.table(table)
        .select("*")
        .eq('sum_period1', fh_q_dict[category]['sum_period1'])
        .gt('sum_normaltime', target)
        .gte("sum_expected_goals_1st", fh_q_dict[category]['sum_expected_goals_1st'][0]).lte("sum_expected_goals_1st", fh_q_dict[category]['sum_expected_goals_1st'][1])
        .gte("sum_1st_shotsongoal", fh_q_dict[category]['sum_1st_shotsongoal'][0]).lte("sum_1st_shotsongoal", fh_q_dict[category]['sum_1st_shotsongoal'][1])
        .gte("sum_1st_totalshotsinsidebox", fh_q_dict[category]['sum_1st_totalshotsinsidebox'][0]).lte("sum_1st_totalshotsinsidebox", fh_q_dict[category]['sum_1st_totalshotsinsidebox'][1])
        .gte("sum_1st_finalthirdentries", fh_q_dict[category]['sum_1st_finalthirdentries'][0]).lte("sum_1st_finalthirdentries", fh_q_dict[category]['sum_1st_finalthirdentries'][1])
        
        .execute()
        )

    elif category == 'yellowcards':
        atual = fh_q_dict[category]['sum_1st_yellowcards'][2]
        target = atual + soma
        response = (
        supabase.table(table)
        .select("*")
        .eq('sum_1st_yellowcards', fh_q_dict[category]['sum_1st_yellowcards'][2])
        .gt('sum_all_yellowcards', target)                     
        .gte("sum_1st_freekicks", fh_q_dict[category]['sum_1st_freekicks'][0]).lte("sum_1st_freekicks", fh_q_dict[category]['sum_1st_freekicks'][1])
        .gte("sum_1st_finalthirdentries", fh_q_dict[category]['sum_1st_finalthirdentries'][0]).lte("sum_1st_finalthirdentries", fh_q_dict[category]['sum_1st_finalthirdentries'][1])
        
        .execute()
    )

    return len(response.data)


def get_under_filter(fh_q_dict, category, soma):
    if category == 'corners':
            atual = fh_q_dict[category]['sum_1st_cornerkicks'][2] 
            target = atual + soma
            response = (
            supabase.table(table)
            .select("*") 
            .eq('sum_period1', fh_q_dict[category]['sum_period1'])
            .eq('sum_1st_cornerkicks', fh_q_dict[category]['sum_1st_cornerkicks'][2])
            .lt('sum_all_cornerkicks', target)
            .gte("sum_1st_totalshotsongoal", fh_q_dict[category]['sum_1st_totalshotsongoal'][0]).lte("sum_1st_totalshotsongoal", fh_q_dict[category]['sum_1st_totalshotsongoal'][1])
            
            .execute()
        )
    elif category == 'gols':
        atual = fh_q_dict[category]['sum_period1']
        target = atual + soma
        response = (
        supabase.table(table)
        .select("*")
        .eq('sum_period1', fh_q_dict[category]['sum_period1'])
        .lt('sum_normaltime', target)
        .gte("sum_expected_goals_1st", fh_q_dict[category]['sum_expected_goals_1st'][0]).lte("sum_expected_goals_1st", fh_q_dict[category]['sum_expected_goals_1st'][1])
        .gte("sum_1st_shotsongoal", fh_q_dict[category]['sum_1st_shotsongoal'][0]).lte("sum_1st_shotsongoal", fh_q_dict[category]['sum_1st_shotsongoal'][1])
        .gte("sum_1st_totalshotsinsidebox", fh_q_dict[category]['sum_1st_totalshotsinsidebox'][0]).lte("sum_1st_totalshotsinsidebox", fh_q_dict[category]['sum_1st_totalshotsinsidebox'][1])
        .gte("sum_1st_finalthirdentries", fh_q_dict[category]['sum_1st_finalthirdentries'][0]).lte("sum_1st_finalthirdentries", fh_q_dict[category]['sum_1st_finalthirdentries'][1])
        
        .execute()
        )

    elif category == 'yellowcards':
        atual = fh_q_dict[category]['sum_1st_yellowcards'][2]
        target = atual + soma
        response = (
        supabase.table(table)
        .select("*")
        .eq('sum_1st_yellowcards', fh_q_dict[category]['sum_1st_yellowcards'][2])
        .lt('sum_all_yellowcards', target)                     
        .gte("sum_1st_freekicks", fh_q_dict[category]['sum_1st_freekicks'][0]).lte("sum_1st_freekicks", fh_q_dict[category]['sum_1st_freekicks'][1])
        .gte("sum_1st_finalthirdentries", fh_q_dict[category]['sum_1st_finalthirdentries'][0]).lte("sum_1st_finalthirdentries", fh_q_dict[category]['sum_1st_finalthirdentries'][1])
        
        .execute()
    )

    return len(response.data)


def get_filter(fh_q_dict, category, soma):
    over_filter = get_over_filter(fh_q_dict, category, soma)
    under_filter = get_under_filter(fh_q_dict, category, soma)
    return over_filter, under_filter