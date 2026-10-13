from src.api.riot_client import get_puuid, get_match_ids, get_match
from src.processing.parser import match_to_row
from src.processing.stats_engine import prepare_dataframe, get_champion_stats, get_win_loss_metrics
from src.ui.dashboard import display_summary, display_champion_stats, display_win_loss_metrics, display_error

GAME_NAME = "ADAM ZEUS KIIN"
TAG_LINE = "soloq"
QUEUE = 420       # 420 = ranked solo/duo, None = tous les modes
COUNT = 100       # nombre de parties demandées (max 100)
MIN_GAMES = 3     # un champion n'apparaît que s'il a au moins X parties

def main():
    # 1. API Calls
    puuid = get_puuid(GAME_NAME, TAG_LINE)
    match_ids = get_match_ids(puuid, count=COUNT, queue=QUEUE)
    print(f"{len(match_ids)} parties trouvées (queue={QUEUE})")

    if not match_ids:
        display_error("Aucune partie pour ce filtre : vérifiez QUEUE, GAME_NAME et TAG_LINE")
        return

    # 2. Parsing
    rows = [match_to_row(get_match(mid), puuid) for mid in match_ids]

    # 3. Processing (Calculs Pandas)
    df = prepare_dataframe(rows)
    champ_stats = get_champion_stats(df, MIN_GAMES)
    win_loss_metrics = get_win_loss_metrics(df)

    # 4. Interface (Affichage)
    display_summary(len(df), df['win'].mean())
    display_champion_stats(champ_stats, MIN_GAMES)
    display_win_loss_metrics(win_loss_metrics)

if __name__ == "__main__":
    main()