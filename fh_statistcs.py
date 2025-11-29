import os
import sys
import time
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def get_statistc_values(fh_statistic,s_key):
    for  i,group in enumerate(fh_statistic):
        for statistc in group['statisticsItems']:
            if statistc['key'] == s_key:                        
                return (statistc['homeValue'],statistc['awayValue'])



def get_FH_statistcs(event_id):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://api.sofascore.com/api/v1/event/{event_id}/statistics"
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    total_itens_txt = soup.find('pre')
    driver.close()

    home_statics_dict = {}
    away_statics_dict = {}

    # Atribuir o conteúdo JSON da tag "pre" a uma variável
    json_text = total_itens_txt.text

    # Parsear o texto JSON para objeto Python
    json_content = json.loads(json_text)

    dict_content = dict(json_content)
    list_statistcs = dict_content["statistics"]
    
    fh_statistic = list_statistcs[1]['groups']
    try:    
        home_statics_dict['Ball possession'], away_statics_dict['Ball possession'] = get_statistc_values(fh_statistic,'ballPossession')
    except:
        home_statics_dict['Ball possession'], away_statics_dict['Ball possession'] = 0,0
    try:
        home_statics_dict['Expected goals'], away_statics_dict['Expected goals'] = get_statistc_values(fh_statistic,'expectedGoals')
    except:
        home_statics_dict['Expected goals'], away_statics_dict['Expected goals'] = 0,0

    try:
        home_statics_dict['Total shots'], away_statics_dict['Total shots'] = get_statistc_values(fh_statistic,'totalShotsOnGoal')
    except:
        home_statics_dict['Total shots'], away_statics_dict['Shots on target'] = 0,0
    try:
        home_statics_dict['Shots on target'], away_statics_dict['Shots on target'] = get_statistc_values(fh_statistic,'shotsOnGoal')
    except:
        home_statics_dict['Shots on target'], away_statics_dict['Shots on target'] = 0,0
    
    try:
        home_statics_dict['Shots inside box'], away_statics_dict['Shots inside box'] = get_statistc_values(fh_statistic,'totalShotsInsideBox')
    except:
        home_statics_dict['Shots inside box'], away_statics_dict['Shots inside box'] = 0,0

    try:
        home_statics_dict['Final third entries'], away_statics_dict['Final third entries'] = get_statistc_values(fh_statistic,'finalThirdEntries')
    except:
        home_statics_dict['Final third entries'], away_statics_dict['Final third entries'] = 0,0
    try:
        home_statics_dict['cornerKicks'], away_statics_dict['cornerKicks'] = get_statistc_values(fh_statistic,'cornerKicks')
    except:
        home_statics_dict['cornerKicks'], away_statics_dict['cornerKicks'] = get_statistc_values(fh_statistic,'cornerKicks')

    try:    
        home_statics_dict['fouls'], away_statics_dict['fouls'] = get_statistc_values(fh_statistic,'fouls')
    except:
        home_statics_dict['fouls'], away_statics_dict['fouls'] = 0,0

    try:
        home_statics_dict['yellowCards'], away_statics_dict['yellowCards'] = get_statistc_values(fh_statistic,'yellowCards')
    except:
        home_statics_dict['yellowCards'], away_statics_dict['yellowCards'] = 0,0

    return home_statics_dict, away_statics_dict



if __name__ == "__main__":
    event_id = input("Digite o event ID: ")
    print(get_FH_statistcs(event_id))
