"""
Módulo de configuração centralizado.
Centraliza conexões e configurações compartilhadas entre módulos.
"""
import os
from supabase import create_client, Client
from typing import Optional, Tuple

# Nome da tabela principal
TABLE_STATICS = 'table_statics'

# Instância singleton do cliente Supabase
_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Retorna uma instância singleton do cliente Supabase.
    
    Returns:
        Client: Cliente Supabase configurado
        
    Raises:
        ValueError: Se as variáveis de ambiente não estiverem configuradas
    """
    global _supabase_client
    
    if _supabase_client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError(
                "Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY devem estar configuradas"
            )
        
        _supabase_client = create_client(url, key)
    
    return _supabase_client


def get_telegram_config() -> Tuple[str, str]:
    """
    Retorna configuração do Telegram.
    
    Returns:
        tuple: (token, chat_id)
        
    Raises:
        ValueError: Se as variáveis de ambiente não estiverem configuradas
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        raise ValueError(
            "Variáveis de ambiente TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID devem estar configuradas"
        )
    
    return token, chat_id

