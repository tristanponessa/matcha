import sqlite_db
import fakedb

from typing import List, Dict


def exec_db(db_name: str, cmd: str, *args) -> List[Dict[str, str]]:
    db = {'sqlite': sqlite_db.exec_sql, 'fakedb ': fakedb.exec_cmd}
    return db[db_name](cmd, *args)
