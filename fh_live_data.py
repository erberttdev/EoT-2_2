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
from fh_id_data import fh_id_data

def fh_live_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://api.sofascore.com/api/v1/sport/football/events/live"
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    total_itens_txt = soup.find('pre')
    driver.close()

    try:
        df = pd.read_csv('tournaments.csv')
        valid_tournament_ids = set(df['tournament_id'].astype(str).tolist())
    except Exception as e:
        print(f"❌ Erro ao carregar torneios: {e}")
        valid_tournament_ids = set()

    # Atribuir o conteúdo JSON da tag "pre" a uma variável
    json_text = total_itens_txt.text
    # Parsear o texto JSON para objeto Python
    json_content = json.loads(json_text)
    dict_content = dict(json_content)
    list_events = dict_content["events"]

    events_dict = {}
    events_lists = []
    for i,event in enumerate(list_events):
        if event['status']['description'] == 'Halftime' and str(event['tournament']['uniqueTournament']['id']) in valid_tournament_ids:
            event_id = event['id']
            print(event_id)
            events_dict = fh_id_data(event_id)
            # events_lists.append(events_dict)
            events_lists.append(event_id)


    return events_lists

if __name__ == "__main__":
    print(fh_live_data())



