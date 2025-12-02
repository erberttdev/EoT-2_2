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


def get_enviar_telegram() -> bool:
    """
    Retorna se deve enviar mensagens via Telegram.
    
    Lê a variável de ambiente ENVIAR_TELEGRAM.
    Valores aceitos: "sim", "s", "yes", "y", "true", "1" (case insensitive)
    Qualquer outro valor será considerado False.
    
    Returns:
        bool: True se deve enviar mensagens, False caso contrário
    """
    valor = os.environ.get("ENVIAR_TELEGRAM", "não").strip().lower()
    valores_verdadeiros = ["sim", "s", "yes", "y", "true", "1"]
    return valor in valores_verdadeiros


def get_system_version() -> str:
    """
    Retorna a versão atual do sistema.
    
    V1 - Versão inicial do sistema EoT (End of Time).
    Esta versão estabelece a base do sistema de predições e análises,
    incluindo funcionalidades de coleta de dados, processamento estatístico
    e geração de previsões para eventos esportivos.
    
    Returns:
        str: Nome da versão do sistema (ex: "V1")
    """
    return "V1"

