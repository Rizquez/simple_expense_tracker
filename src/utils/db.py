import sqlite3


def db_query_params(db, query, parameters=()):
    with sqlite3.connect(db) as conn:
        curs = conn.cursor()
        result = curs.execute(query, parameters)
        conn.commit()
    return result


def db_query_simple(db, query):
    with sqlite3.connect(db) as conn:
        curs = conn.cursor()
        result = curs.execute(query)
        conn.commit()
    return result
