"""
Script para verificar os resultados das previsões em predictions.csv
para as linhas onde a coluna 'resultado' está vazia.
"""
import csv
import os
import logging
from fh_id_data import fh_id_data

logger = logging.getLogger(__name__)

CSV_FILENAME = 'predictions.csv'
BACKUP_FILENAME = 'predictions_backup.csv'


def get_actual_value(event_data, categoria):
    """
    Extrai o valor real da estatística baseada na categoria.

    Args:
        event_data: Dicionário com dados do evento
        categoria: Categoria da previsão ('gols', 'escanteios', 'cartão amarelo')

    Returns:
        int: Valor real da estatística ou None se não disponível
    """
    if not event_data or 'home_statistics' not in event_data:
        return None

    home_stats = event_data['home_statistics']
    away_stats = event_data['away_statistics']

    if categoria == 'gols':
        return event_data['home_score'] + event_data['awayScore']
    elif categoria == 'escanteios':
        return home_stats.get('cornerKicks', 0) + away_stats.get('cornerKicks', 0)
    elif categoria == 'cartão amarelo':
        return home_stats.get('yellowCards', 0) + away_stats.get('yellowCards', 0)
    else:
        return None


def determine_result(tipo_previsao, target, actual_value):
    """
    Determina se a previsão foi GREEN ou RED.

    Args:
        tipo_previsao: Tipo da previsão ('Over' ou 'Under')
        target: Valor alvo
        actual_value: Valor real

    Returns:
        str: 'GREEN' se correta, 'RED' se incorreta, ou None se indefinido
    """
    if actual_value is None:
        return None

    if tipo_previsao == 'Over':
        return 'GREEN' if actual_value > target else 'RED'
    elif tipo_previsao == 'Under':
        return 'GREEN' if actual_value < target else 'RED'
    else:
        return None


def verify_empty_predictions():
    """
    Verifica e atualiza as linhas do CSV onde a coluna 'resultado' está vazia.
    """
    if not os.path.exists(CSV_FILENAME):
        logger.error(f'Arquivo {CSV_FILENAME} não encontrado')
        return

    # Criar backup
    print(f"📋 Criando backup do arquivo...")
    with open(CSV_FILENAME, 'r', encoding='utf-8') as original:
        with open(BACKUP_FILENAME, 'w', encoding='utf-8', newline='') as backup:
            backup.write(original.read())
    print(f"✅ Backup criado: {BACKUP_FILENAME}")

    # Ler todas as linhas
    rows = []
    updated_count = 0
    verified_count = 0

    with open(CSV_FILENAME, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        for row in reader:
            resultado = row.get('resultado', '').strip()

            if not resultado:
                # Linha com resultado vazio - verificar
                event_id = row.get('event_id')
                categoria = row.get('categoria')
                tipo_previsao = row.get('tipo_previsao')
                target_str = row.get('target')

                if not all([event_id, categoria, tipo_previsao, target_str]):
                    print(f"⚠️  Dados incompletos para evento {event_id} - pulando")
                    rows.append(row)
                    continue

                try:
                    target = float(target_str)
                except ValueError:
                    print(f"⚠️  Target inválido para evento {event_id} - pulando")
                    rows.append(row)
                    continue

                print(f"🔍 Verificando evento {event_id} - {categoria} {tipo_previsao} {target}")

                # Buscar dados do evento
                event_data = fh_id_data(event_id)

                if event_data:
                    # Calcular valor real
                    actual_value = get_actual_value(event_data, categoria)

                    if actual_value is not None:
                        # Determinar resultado
                        result = determine_result(tipo_previsao, target, actual_value)

                        if result:
                            row['resultado'] = result
                            updated_count += 1
                            print(f"   ✅ Atualizado: {result} (valor real: {actual_value})")
                        else:
                            print(f"   ⚠️  Não foi possível determinar resultado")
                    else:
                        print(f"   ⚠️  Estatísticas não disponíveis")
                else:
                    print(f"   ❌ Erro ao buscar dados do evento")

                verified_count += 1

            rows.append(row)

    # Escrever de volta no arquivo
    if updated_count > 0:
        with open(CSV_FILENAME, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"\n✅ {updated_count} linha(s) verificada(s) e atualizada(s) com sucesso!")
        print(f"📊 Total de linhas verificadas: {verified_count}")
    else:
        print(f"\nℹ️  Nenhuma linha foi atualizada")
        print(f"📊 Total de linhas verificadas: {verified_count}")

    return updated_count


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    print(f"\n{'='*60}")
    print(f"🔍 VERIFICANDO RESULTADOS DAS PREVISÕES")
    print(f"{'='*60}")
    print(f"Arquivo: {CSV_FILENAME}")
    print(f"{'='*60}\n")

    verify_empty_predictions()
