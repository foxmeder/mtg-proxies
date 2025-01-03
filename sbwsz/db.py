from __future__ import annotations

import sqlite3
from pathlib import Path


class SbwszDB:
    """A simple wrapper for sbwsz sqlite3 database."""

    conn = None
    db_file = None

    def __init__(self, db_path):
        self.db_file = Path(db_path)
        if not self.db_file.exists():
            raise FileNotFoundError(f"DB file {self.db_file} does not exist")
        # initialize db
        self.conn = sqlite3.connect(self.db_file)

    def cards_by_name(self, name: str, lang: str) -> list:
        cards = []
        cur = self.conn.cursor()
        cur.execute(
            "SELECT cards.name as card_name,setCode as card_set,number as collector_number, \
                sets.releaseDate as release_date, zhs.language FROM cards \
                LEFT JOIN sets ON sets.code=cards.setCode \
                LEFT JOIN zhs ON zhs.uuid=cards.uuid WHERE cards.name=? AND \
                ( \
                    cards.language='Chinese Simplified' OR \
                    (cards.language='English' AND cards.setCode in ('FDN','LTC','DSK','DSC','BLB')) \
                    OR (zhs.name != '' AND zhs.name is not null) \
                ) order by date(sets.releaseDate) DESC",
            (name,),
        )
        # 获取查询结果并转化为字典
        columns = [column[0] for column in cur.description]
        for row in cur.fetchall():
            cards.append(dict(zip(columns, row)))
        cur.close()
        return cards
