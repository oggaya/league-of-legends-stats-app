def display_summary(total_games, winrate):
    print(f"\n{total_games} parties analysées, winrate global : {winrate:.0%}")

def display_champion_stats(stats, min_games):
    if stats.empty:
        print(f"Aucun champion avec au moins {min_games} parties")
    else:
        print(stats)

def display_win_loss_metrics(metrics):
    print("\nVictoires (True) vs défaites (False) :")
    print(metrics)

def display_error(message):
    print(f"ERREUR : {message}")