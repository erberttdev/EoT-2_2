import requests
import logging
from config import get_telegram_config

logger = logging.getLogger(__name__)


def enviar_mensagem_telegram(mensagem):
    """
    Envia mensagem via Telegram Bot API.
    
    Args:
        mensagem: Texto da mensagem a enviar
        
    Returns:
        bool: True se enviado com sucesso, False caso contrário
    """
    try:
        token, chat_id = get_telegram_config()
    except ValueError as e:
        logger.error(f"Erro de configuração do Telegram: {e}")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"      └─ ✅ Mensagem enviada com sucesso!")
            logger.info("Mensagem enviada com sucesso via Telegram.")
            return True
        else:
            print(f"      └─ ❌ Erro HTTP {response.status_code}: {response.text}")
            logger.error(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"      └─ ❌ Exceção ao enviar: {e}")
        logger.error(f"Exceção ao enviar mensagem: {e}")
        return False

def formatar_resultado(resultado):
    """
    Formata resultado de previsão para envio via Telegram.
    
    Args:
        resultado: Pode ser um dicionário único ou uma lista de dicionários
        
    Returns:
        str: Mensagem formatada ou None se não houver previsões válidas
    """
    print(f"      └─ 📝 Formatando mensagem...")
    
    # Se for uma lista, processa o primeiro item (compatibilidade com código antigo)
    if isinstance(resultado, list):
        if not resultado or all(not r for r in resultado):
            return None
        # Processa apenas o primeiro resultado da lista
        res = resultado[0] if resultado else None
    else:
        # Se for um dicionário único
        res = resultado
    
    if not res:
        return None
    
    info = res.get('info', {})
    if not info:
        return None
    
    partida = info.get('home_name', 'Desconhecido') + " vs " + info.get('away_name', 'Desconhecido')
    print(f"      └─ 📋 Partida: {partida}")
    
    partida = info.get('home_name', 'Desconhecido') + " vs " + info.get('away_name', 'Desconhecido')
    placar = str(info.get('home_score', 0)) + " - " + str(info.get('awayScore', 0))
    home_stats = info.get('home_statistics', {})
    away_stats = info.get('away_statistics', {})
    corners = str(home_stats.get('cornerKicks', 0)) + " - " + str(away_stats.get('cornerKicks', 0))
    yellow_cards = str(home_stats.get('yellowCards', 0)) + " - " + str(away_stats.get('yellowCards', 0))
    league = info.get('id_tournament', 'Desconhecido')
    gols_over = res.get('gols_over', [])
    gols_under = res.get('gols_under', [])
    corners_over = res.get('corners_over', [])
    corners_under = res.get('corners_under', [])
    yellow_cards_over = res.get('yellowcards_over', [])
    yellow_cards_under = res.get('yellowcards_under', [])

    msg = f"<b>🏟️ {partida}</b>\n\n"
    msg += f"🏆 Torneio: {league}\n"
    msg += f"⚽ Placar intervalo: {placar}\n"
    msg += f"🚩 Corners intervalo: {corners}\n"
    msg += f"🟨 C. Amarelos intervalo: {yellow_cards}\n\n"
    
    if gols_over:
        msg += f"⚽ Gols Over previsões:\n"
        msg += f'Quantidade de gols atuais: {info.get("home_score", 0) + info.get("awayScore", 0)}\n'
        for g in gols_over:
            target = g[0]
            prob = g[2]
            odd = g[3]
            msg += f"- ✅ MAIS que {target}: Prob {int(prob)}%, Odd {odd:.2f}\n"
    
    if gols_under:
        msg += f"\n⚽ Gols Under previsões:\n"
        for g in gols_under[:3]:
            target = g[0]
            prob = g[2]
            odd = g[3]
            msg += f"- 🔻 MENOS que {target}: Prob {int(prob)}%, Odd {odd:.2f}\n"
    
    if corners_over:
        msg += f"\n🚩 Corners Over previsões:\n"
        for c in corners_over:
            target = c[0]
            prob = c[2]
            odd = c[3]
            msg += f"- ✅ MAIS que {target}: Prob {int(prob)}%, Odd {odd:.2f}\n"
    
    if corners_under:
        msg += f"\n🚩 Corners Under previsões:\n"
        for c in corners_under:
            target = c[0]
            prob = c[2]
            odd = c[3]
            msg += f"- 🔻 MENOS que {target}: Prob {int(prob)}%, Odd {odd:.2f}\n"
    
    if yellow_cards_over:
        msg += f"\n🟨 Cartões Amarelos Over previsões:\n"
        for y in yellow_cards_over:
            target = y[0]
            prob = y[2]
            odd = y[3]
            msg += f"- ✅ MAIS que {target}: Prob {int(prob)}%, Odd {odd:.2f}\n"
    
    if yellow_cards_under:
        msg += f"\n🟨 Cartões Amarelos Under previsões:\n"
        for y in yellow_cards_under:
            target = y[0]
            prob = y[2]
            odd = y[3]
            msg += f"- 🔻 MENOS que {target}: Prob {int(prob)}%, Odd {odd:.2f}\n"

    return msg



