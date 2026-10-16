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

def display_rank(rank_data):
    if rank_data is None:
        print("Rank : Non classé (Unranked)")
        return
    tier   = rank_data["tier"]       # ex: GOLD
    rank   = rank_data["rank"]       # ex: II
    lp     = rank_data["leaguePoints"]
    wins   = rank_data["wins"]
    losses = rank_data["losses"]
    total  = wins + losses
    wr     = round(wins / total * 100) if total > 0 else 0
    print(f"Rank : {tier} {rank} — {lp} LP  ({wins}W/{losses}L — {wr}% WR)")
