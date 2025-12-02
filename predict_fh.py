from fh_id_data import fh_id_data
from fh_ca import campo_amostral
from fh_filter import get_filter
from fh_live_data import fh_live_data
from fh_id_predict import over_under
from send_telegram import enviar_mensagem_telegram, formatar_resultado
from save_predictions import save_predictions_to_csv
from update_predictions_results import process_predictions_csv
from config import get_enviar_telegram
import math
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logger = logging.getLogger(__name__)


def filter_min(over_under_resp, min_percent=70, min_odd=1.2):
    """
    Filtra previsões por percentual e odd mínimos.
    
    Args:
        over_under_resp: Resposta com previsões Over/Under
        min_percent: Percentual mínimo
        min_odd: Odd mínima
        
    Returns:
        dict: Dicionário com previsões filtradas
    """

    dict_gols_over = over_under_resp[1]['gols'][0]
    dict_gols_under = over_under_resp[1]['gols'][1]
    dict_corners_over = over_under_resp[2]['corners'][0]
    dict_corners_under = over_under_resp[2]['corners'][1]
    dict_yellow_cards_over = over_under_resp[3]['yellowcards'][0]
    dict_yellow_cards_under = over_under_resp[3]['yellowcards'][1]
    dict_info = over_under_resp[0]
    list_gols_over_resp = []
    list_gols_under_resp = []
    list_corners_over_resp = []
    list_corners_under_resp = []
    list_yellow_cards_over_resp = []
    list_yellow_cards_under_resp = []
    dict_resposta = {}
    for key, value in dict_gols_over.items():
        if (value[2] >= min_percent) and (value[3] >= min_odd):
            list_gols_over_resp.append(dict_gols_over[key])


    for key, value in dict_gols_under.items():
        if (value[2] >= min_percent) and (value[3] >= min_odd):
            list_gols_under_resp.append(dict_gols_under[key])

    for key, value in dict_corners_over.items():
        if (value[2] >= min_percent) and (value[3] >= min_odd):
            list_corners_over_resp.append(dict_corners_over[key])

    for key, value in dict_corners_under.items():
        if (value[2] >= min_percent) and (value[3] >= min_odd):
            list_corners_under_resp.append(dict_corners_under[key])

    for key, value in dict_yellow_cards_over.items():
        if (value[2] >= min_percent) and (value[3] >= min_odd):
            list_yellow_cards_over_resp.append(dict_yellow_cards_over[key])

    for key, value in dict_yellow_cards_under.items():
        if (value[2] >= min_percent) and (value[3] >= min_odd):
            list_yellow_cards_under_resp.append(dict_yellow_cards_under[key])

    if len(list_gols_over_resp) > 0:
        dict_resposta['gols_over'] = list_gols_over_resp
    if len(list_gols_under_resp) > 0:
        dict_resposta['gols_under'] = list_gols_under_resp

    if len(list_corners_over_resp) > 0:
        dict_resposta['corners_over'] = list_corners_over_resp
    if len(list_corners_under_resp) > 0:
        dict_resposta['corners_under'] = list_corners_under_resp
    
    if len(list_yellow_cards_over_resp) > 0:
        dict_resposta['yellowcards_over'] = list_yellow_cards_over_resp
    if len(list_yellow_cards_under_resp) > 0:
        dict_resposta['yellowcards_under'] = list_yellow_cards_under_resp
    
    total_previsoes = (len(list_gols_over_resp) + len(list_gols_under_resp) + 
                      len(list_corners_over_resp) + len(list_corners_under_resp) + 
                      len(list_yellow_cards_over_resp) + len(list_yellow_cards_under_resp))
    
    if total_previsoes > 0:
        dict_resposta['info'] = dict_info
        print(f"      └─ 📊 Filtragem: {len(list_gols_over_resp)} gols_over, {len(list_gols_under_resp)} gols_under")
        print(f"      └─ 📊 Filtragem: {len(list_corners_over_resp)} corners_over, {len(list_corners_under_resp)} corners_under")
        print(f"      └─ 📊 Filtragem: {len(list_yellow_cards_over_resp)} yellowcards_over, {len(list_yellow_cards_under_resp)} yellowcards_under")
        print(f"      └─ ✅ Total: {total_previsoes} previsões válidas após filtragem")

    return dict_resposta


def processar_e_enviar_evento(event_id, min_percent=70, min_odd=1.2):
    """
    Processa um único evento do começo ao fim e envia mensagem individual.
    
    Args:
        event_id: ID do evento a processar
        min_percent: Percentual mínimo para filtrar previsões (padrão: 70)
        min_odd: Odd mínima para filtrar previsões (padrão: 1.2)
        
    Returns:
        bool: True se processado e enviado com sucesso, False caso contrário
    """
    print(f"\n{'='*60}")
    print(f"🏟️  INICIANDO PROCESSAMENTO DO EVENTO: {event_id}")
    print(f"{'='*60}")
    logger.info(f'Processando evento: {event_id}')
    
    try:
        # 1. Obter previsões Over/Under
        print(f"📊 [1/5] Calculando previsões Over/Under...")
        over_under_resp = over_under(event_id)
        print(f"✅ [1/5] Previsões calculadas com sucesso")
        
        # 2. Filtrar previsões por percentual e odd mínimos
        print(f"🔍 [2/5] Filtrando previsões (min_percent={min_percent}%, min_odd={min_odd})...")
        resultado_filtrado = filter_min(over_under_resp, min_percent, min_odd)
        
        # 3. Verificar se há previsões válidas
        if not resultado_filtrado or 'info' not in resultado_filtrado:
            print(f"⚠️  [2/5] Nenhuma previsão válida encontrada após filtragem")
            logger.info(f'Evento {event_id}: Nenhuma previsão válida encontrada')
            return False
        
        num_previsoes = sum([
            len(resultado_filtrado.get('gols_over', [])),
            len(resultado_filtrado.get('gols_under', [])),
            len(resultado_filtrado.get('corners_over', [])),
            len(resultado_filtrado.get('corners_under', [])),
            len(resultado_filtrado.get('yellowcards_over', [])),
            len(resultado_filtrado.get('yellowcards_under', []))
        ])
        print(f"✅ [2/5] {num_previsoes} previsões válidas encontradas")
        
        # 3.5. Salvar previsões no CSV
        print(f"💾 [2.5/5] Salvando previsões no CSV...")
        event_info = resultado_filtrado.get('info', {})
        save_predictions_to_csv(resultado_filtrado, event_info)
        print(f"✅ [2.5/5] Previsões salvas no CSV")

        # 3.6. Atualizar resultados (GREEN/RED) para este event_id
        print(f"🎯 [2.6/5] Atualizando resultados (GREEN/RED) no CSV para event_id={event_id}...")
        process_predictions_csv(event_id_filter=str(event_id))
        print(f"✅ [2.6/5] Resultados atualizados no CSV para event_id={event_id}")
        
        # 4. Formatar resultado
        print(f"📝 [3/5] Formatando mensagem...")
        mensagem = formatar_resultado(resultado_filtrado)
        
        if not mensagem:
            print(f"⚠️  [3/5] Mensagem vazia após formatação")
            logger.info(f'Evento {event_id}: Mensagem vazia após formatação')
            return False
        
        print(f"✅ [3/5] Mensagem formatada ({len(mensagem)} caracteres)")
        
        # 5. Enviar mensagem via Telegram (se habilitado)
        enviar_telegram = get_enviar_telegram()
        if enviar_telegram:
            print(f"📤 [4/5] Enviando mensagem via Telegram...")
            sucesso = enviar_mensagem_telegram(mensagem)
            
            if sucesso:
                print(f"✅ [4/5] Mensagem enviada com sucesso!")
                print(f"✅ [5/5] Processamento concluído com sucesso!")
                print(f"{'='*60}\n")
                logger.info(f'Evento {event_id}: Processado e mensagem enviada com sucesso')
            else:
                print(f"❌ [4/5] Erro ao enviar mensagem")
                print(f"{'='*60}\n")
                logger.warning(f'Evento {event_id}: Erro ao enviar mensagem')
            
            return sucesso
        else:
            print(f"⏭️  [4/5] Envio de mensagem via Telegram desabilitado (ENVIAR_TELEGRAM != sim)")
            print(f"✅ [5/5] Processamento concluído com sucesso!")
            print(f"{'='*60}\n")
            logger.info(f'Evento {event_id}: Processado com sucesso (Telegram desabilitado)')
            return True
        
    except ValueError as e:
        # Erro específico quando não há dados ou estatísticas
        print(f"⚠️  ERRO: {str(e)}")
        print(f"{'='*60}\n")
        logger.warning(f'Evento {event_id}: {str(e)}')
        return False
    except Exception as e:
        # Outros erros inesperados
        print(f"❌ ERRO INESPERADO: {str(e)}")
        print(f"{'='*60}\n")
        logger.error(f'Erro ao processar evento {event_id}: {e}', exc_info=True)
        return False


def resposts_live(list_ids_live):
    """
    Processa múltiplos eventos e retorna lista de resultados.
    Mantido para compatibilidade, mas recomenda-se usar processar_e_enviar_evento().
    
    Args:
        list_ids_live: Lista de IDs de eventos
        
    Returns:
        list: Lista de resultados filtrados
    """
    list_resposts = []
    for id_live in list_ids_live:
        logger.info(f'Processing live id: {id_live}')
        try:
            over_under_resp = over_under(id_live) 
            list_resposts.append(filter_min(over_under_resp))
        except Exception as e:
            logger.error(f'Error processing id {id_live}: {e}')

    return list_resposts

# def main_task():
#     list_ids_live = fh_live_data()
#     # list_ids_live = [14109730, 14109726,13472608]
#     if len(list_ids_live) > 0:
#         list_resposts_live = resposts_live(list_ids_live)
#         mensagem = formatar_resultado(list_resposts_live)
#         enviar_mensagem_telegram(mensagem)
#     else:
#         print('No live matches found.')


# if __name__ == "__main__":
#     # Configurar logging para APScheduler
#     logging.basicConfig(level=logging.INFO)

#     # Criar scheduler
#     scheduler = BlockingScheduler()

#     # Agendar a tarefa para executar a cada 10 minutos
#     scheduler.add_job(main_task, 'interval', minutes=10)

#     # Executar a tarefa imediatamente na primeira vez
#     main_task()

#     # Iniciar o scheduler
#     scheduler.start()
