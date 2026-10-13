import pandas as pd

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