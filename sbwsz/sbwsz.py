from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from tempfile import gettempdir

from sbwsz.db import SbwszDB

cache = Path(gettempdir()) / "sbwsz_cache"
cache.mkdir(parents=True, exist_ok=True)  # Create cache folder

sbwsz_db = None

_cache = {}

# unofficial translations
unofficial_translations = {
    "fdn": [(1, 175), (177, 271), (357, 361)],
    "fdc": [],
    "blb": [],
    "dsc": [(1, 94)],
    "dsk": [],
    "ltc": [],
}


def set_cache_path(path: str):
    """Set the path to the cache folder.
    Defaults to `~/.cache/sbwsz_cache`.
    Args:
        path: Path to cache folder
    """

    if path == "":
        return
    global cache, sbwsz_db
    cache = Path(path) / "sbwsz_cache"
    cache.mkdir(parents=True, exist_ok=True)
    db_file = cache / "zhs.sqlite"
    print(f"Using sbwsz DB {db_file}")
    sbwsz_db = SbwszDB(db_file)


def unoffical_exists(card: dict) -> bool:
    global unofficial_translations
    if not card["collector_number"].isdigit():
        return False
    card_set = card["card_set"].lower()
    if card_set in unofficial_translations:
        if len(unofficial_translations[card_set]) == 0:
            return True
        for range in unofficial_translations[card_set]:
            collector_number = int(card["collector_number"])
            if collector_number >= range[0] and collector_number <= range[1]:
                return True
        return False
    if card["language"] == "MTGso":
        # MTGso translations are not official
        return False
    return True


@lru_cache(maxsize=None)
def unoficial_zhs_set():
    global unofficial_translations
    return unofficial_translations.keys()


def recommend_print(current=None, card_name: str | None = None, oracle_id: str | None = None, mode="best"):
    global sbwsz_db, _cache
    if card_name in _cache:
        return _cache[card_name]
    if sbwsz_db is None:
        return None
    cards = sbwsz_db.cards_by_name(card_name, "zhs")
    cards = [c for c in cards if unoffical_exists(c)]
    card = cards[0] if len(cards) > 0 else None
    _cache[card_name] = card
    return card
