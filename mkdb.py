import argparse
from pathlib import Path

import ijson

import localfile
import scryfall
from scryfall.db import ScryfallDb


def make_local_scan_db(local_scan_path, db_file):
    scan_path = Path(local_scan_path)
    scan_path.walk(lambda path, dirs, files: [])


def make_scryfall_db(all_cards_file, db_file):
    print(f"reading {all_cards_file}")
    with open(all_cards_file, encoding="UTF-8") as f:
        # parser = ijson.parse(f)
        # for prefix, event, value in parser:
        #     print(f"Prefix: {prefix}, Event: {event}, Value: {value}")
        all_cards = ijson.items(f, "item", use_float=True)
        db = ScryfallDb(db_file)
        i = 0
        cards = []
        for card in all_cards:
            i += 1
            print(f'add {i} {card["name"]}' + " " * (100 - len(card["name"])) + "\r", end="")
            cards.append(card)
            if i % 1000 == 0:
                db.add_cards(cards)
                cards = []
        # the rest of the cards
        db.add_cards(cards)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="initialize sqlite3 db for printing.")
    parser.add_argument(
        "db_type",
        type=str,
        help="db type (default: %(default)s)",
        default="scryfall",
        choices=["scryfall", "local_scan"],
    )
    parser.add_argument("--cache_path", type=str, help="path to cache directory", default="./.cache")
    parser.add_argument("--local_scan_path", type=str, help="path to local scan directory", default=None)
    parser.add_argument("--all_cards", type=str, help="path to all_cards.json", default=None)
    args = parser.parse_args()
    scryfall.set_cache_path(args.cache_path)
    cache_path = Path(args.cache_path)
    if args.db_type == "scryfall":
        if args.all_cards is None:
            raise ValueError("--all_cards is required for scryfall db.")
        db_file = cache_path / "scryfall.db"
        print(f"Initializing Scryfall DB {db_file}...")
        make_scryfall_db(args.all_cards, cache_path / "scryfall_cache/scryfall.db")
        print("Scryfall DB initialized.")
    else:
        if args.local_scan_path is None:
            raise ValueError("--local_scan_path is required for local_scan db.")
        localfile.set_local_scan_path(args.local_scan_path, cache_path / "local_scan.db")
        make_local_scan_db()
        print("Local scan DB initialized.")
