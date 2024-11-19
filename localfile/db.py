from __future__ import annotations

import sqlite3
from pathlib import Path


class LocalScanDB:
    db_file = None
    conn = None

    def __init__(self, db_path, cards=None) -> None:
        self.db_file = Path(db_path)
        self.conn = sqlite3.connect(self.db_file)
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS cards (name TEXT, set TEXT, local_path TEXT)")
        cur.execute("CREATE INDEX IF NOT EXISTS name_idx ON cards (name)")
        cur.close()
        if cards is not None:
            self.add_cards(cards)

    def add_cards(self, cards) -> None:
        cur = self.conn.cursor()
        rows = [(card["name"], card["set"], card["local_path"]) for card in cards]
        cur.executemany("INSERT INTO cards VALUES (?, ?, ?)", rows)
        self.conn.commit()
        cur.close()

    def get_card(self, card_name, set):
        with self.conn.cursor() as cur:
            cur.execute("SELECT local_path FROM cards WHERE name=? AND set=?", (card_name, set))
            data = cur.fetchone()
            return {"name": card_name, "set": set, "local_path": data[0]} if data else None

    def __exit__(self) -> None:
        self.conn.close()
