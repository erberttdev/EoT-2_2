import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fh_statistcs import get_FH_statistcs



def fh_id_data(even_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://api.sofascore.com/api/v1/event/{even_id}"
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    total_itens_txt = soup.find('pre')
    driver.close()


    # Atribuir o conteúdo JSON da tag "pre" a uma variável
    json_text = total_itens_txt.text
    # Parsear o texto JSON para objeto Python
    json_content = json.loads(json_text)
    dict_content = dict(json_content)
    list_events = dict_content["event"]
    # print(list_events)

    events_dict = {}
    # print(list_events)
    events_dict['event_id'] = list_events['id']
    events_dict['id_tournament'] = list_events['tournament']['uniqueTournament']['id']
    events_dict['id_tournament'] = list_events['tournament']['uniqueTournament']['name']
    events_dict['home_name'] = list_events['homeTeam']['name']
    events_dict['away_name'] = list_events['awayTeam']['name']
    events_dict['home_score'] = list_events['homeScore']['period1']
    events_dict['awayScore'] = list_events['awayScore']['period1']
    # events_dict['normaltime'] = list_events['homeScore']['normaltime']
    # events_dict['normaltime'] = list_events['awayScore']['normaltime']

    try:
        events_dict['home_statistics'], events_dict['away_statistics'] = get_FH_statistcs(events_dict['event_id'])
    except:
        print(f'Sem estatisticas para {events_dict['event_id']}')
        events_dict = None
        # events_dict['home_statistics'] = {'Expected goals': 0, 'Total shots': 0, 'Shots on target': 0, 'Shots inside box': 0, 'Final third entries': 0, 'cornerKicks': 0, 'fouls': 0, 'yellowCards': 0}
        # events_dict['away_statistics'] = {'Expected goals': 0, 'Total shots': 0, 'Shots on target': 0, 'Shots inside box': 0, 'Final third entries': 0, 'cornerKicks': 0, 'fouls': 0, 'yellowCards': 0}
        
    return events_dict



if __name__ == "__main__":

    event_id = input("Digite o event ID: ")
    print(fh_id_data(event_id))



