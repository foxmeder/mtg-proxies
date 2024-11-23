from __future__ import annotations

import json
import sqlite3
from pathlib import Path


class ScryfallDb:
    """A simple SQLite database wrapper for the Scryfall Bulk Data."""

    conn = None
    db_file = None

    def __init__(self, db_path, cards=None) -> None:
        global cache
        self.db_file = Path(db_path)
        alreay_init = self.db_file.exists()
        # initialize db
        self.conn = sqlite3.connect(self.db_file)
        if alreay_init:
            return
        cur = self.conn.cursor()
        print("Initializing DB")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS cards ( \
                id TEXT PRIMARY KEY, oracle_id TEXT, card_name TEXT ,printed_name TEXT, card_set TEXT, \
                collector_number TEXT,lang TEXT, released_at TEXT, data TEXT \
            )"
        )
        cur.execute("CREATE INDEX IF NOT EXISTS oracle_id_idx ON cards (oracle_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS name_idx ON cards (card_name)")

        if cards is None:
            return
        # insert cards into db batch
        self.add_cards(cards)
        cur.close()

    def add_cards(self, cards):
        cur = self.conn.cursor()
        rows = []
        for card in cards:
            card_data = json.dumps(card)
            rows.append(
                (
                    card["id"],
                    card["oracle_id"] if "oracle_id" in card else "",
                    card["name"],
                    card["printed_name"] if "printed_name" in card else "",
                    card["set"],
                    card["collector_number"],
                    card["lang"],
                    card["released_at"],
                    card_data,
                )
            )
        cur.executemany("REPLACE INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
        self.conn.commit()
        cur.close()

    def cards_by_oracle_id(self, oracle_id: str, lang: str):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT data FROM cards WHERE oracle_id=? AND lang=? \
                order by date(released_at) DESC",
            (oracle_id, lang),
        )
        cards = cur.fetchall()
        if lang != "en" and len(cards) == 0:
            cur.execute(
                "SELECT data FROM cards WHERE oracle_id=? AND lang='en' order by date(released_at) DESC",
                (oracle_id,),
            )
            cards += cur.fetchall()
        cur.close()
        return [json.loads(card[0]) for card in cards]

    def cards_by_name(self, name: str, lang: str) -> list:
        cards = []
        cur = self.conn.cursor()
        cur.execute(
            "SELECT data FROM cards WHERE card_name=? AND (lang=? OR lang='en') \
                    order by date(released_at) DESC",
            (name, lang),
        )
        cards = cur.fetchall()
        cur.close()
        return [json.loads(card[0]) for card in cards]

    def double_faced_by_front(self, name: str, lang: str):
        cards = []
        cur = self.conn.cursor()
        sql = "SELECT data FROM cards WHERE card_name like ? AND lang=? order by date(released_at) DESC"
        cur.execute(sql, (f"{name} //%", lang))
        cards = cur.fetchall()
        cur.close()
        return [json.loads(card[0]) for card in cards]

    def get_cards(self, lang: str, **kwargs) -> list:
        cards = []
        cur = self.conn.cursor()
        wheres = ""
        params = []
        for key, value in kwargs.items():
            if not value:
                continue
            if key == "set":
                wheres += " AND card_set=?"
                params.append(value.lower())
            elif key == "collector_number":
                wheres += " AND collector_number=?"
                params.append(value)
        sql = f"SELECT data FROM cards WHERE card_name=? {wheres} AND lang=? \
                order by date(released_at) DESC"
        cur.execute(sql, (kwargs["name"],) + tuple(params) + (lang,))
        cards = cur.fetchall()
        if lang != "en":
            sql = f"SELECT data FROM cards WHERE card_name=? {wheres} AND lang='en' \
                order by date(released_at) DESC"
            cur.execute(sql, (kwargs["name"],) + tuple(params))
            cards += cur.fetchall()
        cur.close()
        return [json.loads(card[0]) for card in cards]

    def __exit__(self):
        self.conn.close()
