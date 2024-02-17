from model.database import pool
import sqlalchemy

def execute(cmd_text, param={}) -> list:
    cmd = sqlalchemy.text(cmd_text)
    with pool.connect() as db_conn:
        result = db_conn.execute(cmd, param).fetchall()
    
    return result

def executeNoneQuery(cmd_text, param={}) -> None:
    cmd = sqlalchemy.text(cmd_text)

    with pool.connect() as db_conn:
        db_conn.execute(cmd, param)
        db_conn.commit()

def _list2dict(result: list, names):
    r = []
    for row in result:
        r.append({k: v for k, v in zip(names, row)})
    return r