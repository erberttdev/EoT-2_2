import os
import json
import requests

def enviar_mensagem_telegram(mensagem):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Erro: Variáveis de ambiente TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID não estão definidas.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "HTML"  # Para formatação básica
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso via Telegram.")
            return True
        else:
            print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exceção ao enviar mensagem: {e}")
        return False

def formatar_resultado(resultado):
    if not resultado or all(not r for r in resultado):
        return "Nenhuma previsão disponível no momento."

    mensagens = []
    for i, res in enumerate(resultado):
        if res:
            info = res.get('info', {})
            partida = info.get('home_name', 'Desconhecido') + " vs " + info.get('away_name', 'Desconhecido')
            placar = str(info.get('home_score', '0')) + " - " + str(info.get('away_score', '0'))
            corners = str(info.get('corners_home', '0')) + " - " + str(info.get('corners_away', '0'))
            yellow_cards = str(info.get('yellow_cards_home', '0')) + " - " + str(info.get('yellow_cards_away', '0'))
            league = info.get('id_tournament', 'Desconhecido')
            gols_over = res.get('gols_over', [])
            gols_under = res.get('gols_under', [])
            corners_over = res.get('corners_over', [])
            corners_under = res.get('corners_under', [])

            msg = f"<b>Partida: {partida}</b>\n\n"
            if info:
                msg += f"Torneio: {league}\n"
                # msg += f"Partida: {partida}\n"
                msg += f"Placar intervalo: {placar}\n"
                msg += f"Corners intervalo: {corners}\n"
                msg += f"C. Amarelos intervalo: {yellow_cards}\n\n"
                # msg += f"Informações: {json.dumps(info, indent=2)}\n"
            if gols_over:
                msg += f"Gols Over previsões:\n"
                msg += f'Quantidade de gols atuais: {info.get('home_score',0) + info.get('away_score',0)}\n'
                for g in gols_over:
                    target = g[0]
                    prob = g[2]
                    odd = g[3]
                    msg += f"- Over {target}: Prob {prob:.2f}%, Odd {odd:.2f}\n"
            if gols_under:
                msg += f"Gols Under previsões:\n"
                for g in gols_under[:3]:
                    target = g[0]
                    prob = g[2]
                    odd = g[3]
                    msg += f"- Under {target}: Prob {prob:.2f}%, Odd {odd:.2f}\n"
            if corners_over:
                msg += f"Corners Over previsões:\n"
                for c in corners_over:
                    target = c[0]
                    prob = c[2]
                    odd = c[3]
                    msg += f"- Over {target}: Prob {prob:.2f}%, Odd {odd:.2f}\n"
            if corners_under:
                msg += f"Corners Under previsões:\n"
                for c in corners_under:
                    target = c[0]
                    prob = c[2]
                    odd = c[3]
                    msg += f"- Under {target}: Prob {prob:.2f}%, Odd {odd:.2f}\n"


            mensagens.append(msg)

    return "\n\n".join(mensagens) if mensagens else "Nenhuma previsão válida encontrada."



