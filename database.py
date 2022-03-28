import sqlite3

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS renewable (id INTEGER PRIMARY KEY, date DATE, total INTEGER, renewable INTEGER, pTotal INTEGER, pRenewable INTEGER);"

INSERT = "INSERT INTO renewable(date, total, renewable, pTotal, pRenewable) VALUES (?, ?, ?, ?, ?);"

GET_ALL = "SELECT * FROM renewable;"
GET_BY_DATE = "SELECT * FROM renewable WHERE date >= ? and date <= ?;"
DELETE_BY_ID = "DELETE from renewable WHERE id >= ? and id <=? "
def connect():
    return sqlite3.connect("data.db")

def create_tables(connection):
    with connection:
        connection.execute(CREATE_TABLE)

def add_value(connection, date, total, renewable, pTotal, pRenewable):
    with connection:
        connection.execute(INSERT, (date, total, renewable, pTotal, pRenewable))

def get_all(connection):
    with connection:
        return connection.execute(GET_ALL).fetchall()

def get_by_date(connection, start, end):
    with connection:
        return connection.execute(GET_BY_DATE, (start, end)).fetchall()
def delete_by_id(connection, startId, endId):
    with connection:
        return connection.execute(DELETE_BY_ID, (startId, endId))