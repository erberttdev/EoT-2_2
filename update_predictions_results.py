import csv
from typing import List, Dict, Any, Optional

from web_scraper import fetch_api_data
from fh_statistcs import get_FH_statistcs


def get_total_goals(event_id: str) -> Optional[float]:
    """
    Busca o total de gols (tempo normal) de um evento.

    Usa a mesma abordagem de `fh_id_data`, acessando a chave "event".
    """
    try:
        data = fetch_api_data(f"/api/v1/event/{event_id}")
    except Exception as e:
        print(f"[ERRO] Falha ao buscar dados de gols para event_id={event_id}: {e}")
        return None

    try:
        event_data = data.get("event") or {}
        home_score = event_data.get("homeScore") or {}
        away_score = event_data.get("awayScore") or {}

        # Usuário pediu normaltime
        home = home_score.get("normaltime")
        away = away_score.get("normaltime")

        if home is None or away is None:
            return None

        return float(home) + float(away)
    except Exception as e:
        print(f"[ERRO] Estrutura inesperada em /event para event_id={event_id}: {e}")
        return None


def get_total_corners(event_id: str) -> Optional[float]:
    """
    Busca o total de escanteios do evento usando a mesma lógica
    de estatísticas do primeiro tempo de `get_FH_statistcs`.
    """
    try:
        home_stats, away_stats = get_FH_statistcs(event_id)
    except Exception as e:
        print(f"[ERRO] Falha ao buscar estatísticas (FH) de escanteios para event_id={event_id}: {e}")
        return None

    if not home_stats and not away_stats:
        return None

    # Em get_FH_statistcs, a chave é 'cornerKicks'
    home = home_stats.get("cornerKicks")
    away = away_stats.get("cornerKicks")

    if home is None or away is None:
        return None

    try:
        return float(home) + float(away)
    except (TypeError, ValueError):
        return None


def get_total_yellow_cards(event_id: str) -> Optional[float]:
    """
    Busca o total de cartões amarelos do evento usando a mesma lógica
    de estatísticas do primeiro tempo de `get_FH_statistcs`.
    """
    try:
        home_stats, away_stats = get_FH_statistcs(event_id)
    except Exception as e:
        print(f"[ERRO] Falha ao buscar estatísticas (FH) de cartões para event_id={event_id}: {e}")
        return None

    if not home_stats and not away_stats:
        return None

    # Em get_FH_statistcs, a chave é 'yellowCards'
    home = home_stats.get("yellowCards")
    away = away_stats.get("yellowCards")

    if home is None or away is None:
        return None

    try:
        return float(home) + float(away)
    except (TypeError, ValueError):
        return None


def avaliar_over_under(tipo_previsao: str, target: float, valor_real: float) -> str:
    """
    Retorna 'GREEN' ou 'RED' para uma aposta Over/Under.

    Regra adotada:
      - Over: GREEN se valor_real > target, senão RED
      - Under: GREEN se valor_real < target, senão RED
    """
    tp = (tipo_previsao or "").strip().lower()
    if tp == "over":
        return "GREEN" if valor_real > target else "RED"
    elif tp == "under":
        return "GREEN" if valor_real < target else "RED"
    else:
        # Tipo desconhecido: consideramos RED por segurança
        return "RED"


def process_predictions_csv(
    csv_filename: str = "predictions.csv",
    event_id_filter: Optional[str] = None,
):
    """
    Lê o CSV de previsões, busca linhas com 'resultado' vazio e preenche
    com GREEN ou RED consultando a API da SofaScore.
    """
    rows: List[Dict[str, Any]] = []

    # 1. Ler CSV
    with open(csv_filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or [
            "event_id",
            "tournament_id",
            "categoria",
            "tipo_previsao",
            "target",
            "prob",
            "resultado",
        ]

        for row in reader:
            rows.append(row)

    # 2. Processar linhas com resultado vazio
    for row in rows:
        resultado_atual = (row.get("resultado") or "").strip()
        if resultado_atual:
            # Já preenchido
            continue

        event_id = str(row.get("event_id") or "").strip()

        # Se foi passado um filtro de event_id, só processa esse
        if event_id_filter is not None and event_id != str(event_id_filter):
            continue
        categoria = (row.get("categoria") or "").strip().lower()
        tipo_previsao = row.get("tipo_previsao") or row.get("tipo_previsão") or ""
        target_raw = row.get("target")

        if not event_id:
            print("[AVISO] Linha sem event_id, ignorando.")
            continue

        try:
            target = float(target_raw)
        except (TypeError, ValueError):
            print(
                f"[AVISO] Target inválido ('{target_raw}') para event_id={event_id}, "
                "não foi possível avaliar."
            )
            continue

        print(
            f"Processando event_id={event_id} | categoria={categoria} | "
            f"tipo={tipo_previsao} | target={target}"
        )

        valor_real: Optional[float] = None

        if categoria == "gols":
            valor_real = get_total_goals(event_id)
        elif categoria == "escanteios":
            valor_real = get_total_corners(event_id)
        elif categoria == "cartão amarelo":
            valor_real = get_total_yellow_cards(event_id)
        else:
            print(f"[AVISO] Categoria desconhecida '{categoria}' para event_id={event_id}, ignorando.")
            continue

        if valor_real is None:
            print(
                f"[AVISO] Não foi possível obter valor_real para event_id={event_id}, "
                "resultado permanecerá vazio."
            )
            continue

        resultado = avaliar_over_under(tipo_previsao, target, valor_real)
        row["resultado"] = resultado

        print(
            f"  -> valor_real={valor_real} => resultado={resultado}"
        )

    # 3. Regravar CSV (sobrescrevendo) com os resultados atualizados
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"\nConcluído. Arquivo '{csv_filename}' atualizado com resultados GREEN/RED onde possível.")


if __name__ == "__main__":
    process_predictions_csv()


