import logging
import traceback
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('football_prediction_system')

def format_error_message(error: Exception) -> str:
    """Formata mensagens de erro para logging"""
    try:
        error_type = type(error).__name__
        error_message = str(error)
        
        # Obter traceback simplificado
        tb = traceback.extract_tb(error.__traceback__)
        if tb:
            last_frame = tb[-1]
            filename = last_frame.filename.split('/')[-1]  # Pegar apenas o nome do arquivo
            line_number = last_frame.lineno
            location = f"{filename}:{line_number}"
        else:
            location = "unknown location"
        
        return f"{error_type}: {error_message} (at {location})"
        
    except Exception:
        return f"Erro desconhecido: {str(error)}"

def log_system_info():
    """Log informações do sistema"""
    logger.info("=" * 60)
    logger.info("SISTEMA DE PREVISÃO DE ESTATÍSTICAS DE FUTEBOL")
    logger.info(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

def log_processing_summary(processed_games: int, successful_games: int, errors: int):
    """Log resumo do processamento"""
    logger.info("=" * 60)
    logger.info("RESUMO DO PROCESSAMENTO")
    logger.info(f"Total de jogos processados: {processed_games}")
    logger.info(f"Jogos processados com sucesso: {successful_games}")
    logger.info(f"Erros encontrados: {errors}")
    logger.info(f"Taxa de sucesso: {(successful_games/processed_games*100):.1f}%" if processed_games > 0 else "N/A")
    logger.info("=" * 60)

def format_prediction_results(predictions: dict) -> str:
    """Formata resultados de previsão para logging"""
    output = []
    
    if 'goals' in predictions:
        output.append("⚽ PREVISÃO DE GOLS:")
        for category, probability in predictions['goals'].items():
            output.append(f"   {category}: {probability:.1%}")
    
    if 'corners' in predictions:
        output.append("🎯 PREVISÃO DE ESCANTEIOS:")
        for category, probability in predictions['corners'].items():
            output.append(f"   {category}: {probability:.1%}")
    
    return "\n".join(output)

def validate_game_data(game_data: dict) -> bool:
    """Valida dados básicos do jogo"""
    required_fields = ['id', 'homeTeam', 'awayTeam', 'tournament', 'status']
    
    for field in required_fields:
        if field not in game_data:
            logger.warning(f"Campo obrigatório ausente: {field}")
            return False
    
    if 'description' not in game_data['status']:
        logger.warning("Status do jogo sem descrição")
        return False
    
    return True

def format_game_info(game: dict) -> str:
    """Formata informações do jogo para logging"""
    home_team = game.get('homeTeam', {}).get('name', 'Desconhecido')
    away_team = game.get('awayTeam', {}).get('name', 'Desconhecido')
    home_score = game.get('homeScore', {}).get('period1', 0)
    away_score = game.get('awayScore', {}).get('period1', 0)
    tournament = game.get('tournament', {}).get('uniqueTournament', {}).get('name', 'Desconhecido')
    
    return f"{home_team} {home_score}-{away_score} {away_team} ({tournament})"
