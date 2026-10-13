import os
import json
from pathlib import Path
from dotenv import load_dotenv
from riotwatcher import LolWatcher, RiotWatcher

load_dotenv()
KEY = os.getenv("RIOT_API_KEY")

REGION = "euw1"
ROUTING = "europe"

riot = RiotWatcher(KEY)
lol = LolWatcher(KEY)

MATCH_DIR = Path("data/matches")
MATCH_DIR.mkdir(parents=True, exist_ok=True)


def get_puuid(game_name, tag_line):
    return riot.account.by_riot_id(ROUTING, game_name, tag_line)["puuid"]


def get_match_ids(puuid, count=20, queue=None):
    # queue=420 pour ne garder que la ranked solo/duo
    return lol.match.matchlist_by_puuid(ROUTING, puuid, count=count, queue=queue)


def get_match(match_id):
    """Lit la partie depuis le disque si elle existe, sinon l'appelle et la sauvegarde."""
    path = MATCH_DIR / f"{match_id}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    match = lol.match.by_id(ROUTING, match_id)
    path.write_text(json.dumps(match), encoding="utf-8")
    return match