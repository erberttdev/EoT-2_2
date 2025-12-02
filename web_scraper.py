"""
Módulo centralizado para web scraping usando Selenium.
Centraliza a configuração e uso do WebDriver.
"""
import time
import json
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def create_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Cria e retorna uma instância configurada do Chrome WebDriver.
    
    Args:
        headless: Se True, executa o navegador em modo headless
        
    Returns:
        webdriver.Chrome: Instância configurada do WebDriver
    """
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    return driver


def fetch_json_from_url(url: str, wait_time: float = 1.0) -> dict:
    """
    Busca JSON de uma URL usando Selenium e retorna como dicionário.
    
    Args:
        url: URL para buscar
        wait_time: Tempo de espera após carregar a página (em segundos)
        
    Returns:
        dict: Conteúdo JSON parseado
        
    Raises:
        ValueError: Se não conseguir encontrar ou parsear o JSON
    """
    driver = None
    try:
        driver = create_driver()
        driver.get(url)
        time.sleep(wait_time)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        pre_tag = soup.find('pre')
        
        if not pre_tag:
            raise ValueError(f"Não foi possível encontrar conteúdo JSON na URL: {url}")
        
        json_text = pre_tag.text
        json_content = json.loads(json_text)
        
        return dict(json_content)
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao parsear JSON da URL {url}: {e}")
    finally:
        if driver:
            driver.close()


def fetch_api_data(endpoint: str, wait_time: float = 1.0) -> dict:
    """
    Busca dados de um endpoint da API SofaScore.
    
    Args:
        endpoint: Endpoint da API (ex: '/api/v1/event/12345')
        wait_time: Tempo de espera após carregar a página (em segundos)
        
    Returns:
        dict: Dados da API parseados
    """
    base_url = "https://api.sofascore.com"
    full_url = f"{base_url}{endpoint}"
    return fetch_json_from_url(full_url, wait_time)

