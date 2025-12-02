"""
Módulo para carregar e gerenciar lista de torneios válidos.
"""
import pandas as pd
from typing import Set, Optional
import logging

logger = logging.getLogger(__name__)

# Cache para evitar recarregar o arquivo múltiplas vezes
_tournament_cache: Optional[Set[str]] = None
_TOURNAMENT_FILE = 'tournaments.csv'


def load_valid_tournament_ids() -> Set[str]:
    """
    Carrega os IDs de torneios válidos do arquivo CSV.
    
    Returns:
        Set[str]: Conjunto de IDs de torneios válidos (como strings)
    """
    global _tournament_cache
    
    if _tournament_cache is not None:
        return _tournament_cache
    
    try:
        df = pd.read_csv(_TOURNAMENT_FILE)
        _tournament_cache = set(df['tournament_id'].astype(str).tolist())
        logger.info(f"Carregados {len(_tournament_cache)} torneios válidos")
        return _tournament_cache
    except FileNotFoundError:
        logger.warning(f"Arquivo {_TOURNAMENT_FILE} não encontrado. Retornando conjunto vazio.")
        _tournament_cache = set()
        return _tournament_cache
    except Exception as e:
        logger.error(f"Erro ao carregar torneios: {e}")
        _tournament_cache = set()
        return _tournament_cache


def is_valid_tournament(tournament_id: str) -> bool:
    """
    Verifica se um ID de torneio é válido.
    
    Args:
        tournament_id: ID do torneio (como string)
        
    Returns:
        bool: True se o torneio for válido
    """
    valid_ids = load_valid_tournament_ids()
    return tournament_id in valid_ids


def clear_cache():
    """
    Limpa o cache de torneios (útil para testes ou recarregar dados).
    """
    global _tournament_cache
    _tournament_cache = None

