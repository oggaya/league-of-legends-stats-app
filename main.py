import pandas as pd
from riot_client import get_puuid, get_match_ids, get_match

GAME_NAME = "ADAM ZEUS KIIN"
TAG_LINE = "soloq"
QUEUE = 420       # 420 = ranked solo/duo, None = tous les modes
COUNT = 100        # nombre de parties demandées (max 100)
MIN_GAMES = 3     # un champion n'apparaît que s'il a au moins X parties

def match_to_row(match, puuid):
    info = match["info"]
    me = next(p for p in info["participants"] if p["puuid"] == puuid)
    return {
        "match_id": match["metadata"]["matchId"],
        "date": pd.to_datetime(info["gameCreation"], unit="ms"),
        "queue": info["queueId"],
        "duration_min": info["gameDuration"] / 60,
        "champion": me["championName"],
        "role": me["teamPosition"],
        "kills": me["kills"],
        "deaths": me["deaths"],
        "assists": me["assists"],
        "cs": me["totalMinionsKilled"] + me["neutralMinionsKilled"],
        "damage": me["totalDamageDealtToChampions"],
        "vision": me["visionScore"],
        "win": me["win"],
    }


def main():
    puuid = get_puuid(GAME_NAME, TAG_LINE)
    match_ids = get_match_ids(puuid, count=COUNT, queue=QUEUE)
    print(f"{len(match_ids)} parties trouvées (queue={QUEUE})")

    if not match_ids:
        print("Aucune partie pour ce filtre : vérifie QUEUE, GAME_NAME et TAG_LINE")
        return

    rows = [match_to_row(get_match(mid), puuid) for mid in match_ids]
    df = pd.DataFrame(rows)

    # On écarte les remakes et parties très courtes
    df = df[df["duration_min"] > 5].copy()

    df["kda"] = (df["kills"] + df["assists"]) / df["deaths"].clip(lower=1)
    df["cs_min"] = df["cs"] / df["duration_min"]

    stats = (
        df.groupby("champion")
        .agg(
            parties=("win", "size"),
            winrate=("win", "mean"),
            kda=("kda", "mean"),
            morts=("deaths", "mean"),
            cs_min=("cs_min", "mean"),
            degats=("damage", "mean"),
        )
        .sort_values("parties", ascending=False)
        .round(2)
    )
    stats = stats[stats["parties"] >= MIN_GAMES]

    print(f"\n{len(df)} parties analysées, winrate global : {df['win'].mean():.0%}")
    if stats.empty:
        print(f"Aucun champion avec au moins {MIN_GAMES} parties")
    else:
        print(stats)

    df["morts_min"] = df["deaths"] / df["duration_min"] 
    df["dmg_min"] = df["damage"] / df["duration_min"]

    print("\nVictoires (True) vs défaites (False) :")
    print(
        df.groupby("win")
        .agg(
            parties=("win", "size"),
            morts=("deaths", "mean"),
            morts_min=("morts_min", "mean"),
            kda=("kda", "mean"),
            cs_min=("cs_min", "mean"),
            degats=("damage", "mean"),
            duree=("duration_min", "mean"),
            degats_min=("dmg_min", "mean"),
        )
        .round(2)
    )

if __name__ == "__main__":
    main()