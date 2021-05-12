import sqlite3

conn = sqlite3.connect("./src/data.db")


def create():
    cursor = conn.cursor()
    sql = "create table if not exists tax(" \
          "id INTEGER PRIMARY KEY," \
          "commodity varchar(30) unique," \
          "'name' varchar(15) not null ," \
          "code char(19) not null ," \
          "tax_rate float not null);"
    cursor.execute(sql)
    cursor.close()
    conn.commit()


def insert(commodity, name, code, tax_rate):
    cursor = conn.cursor()
    sql = f"replace INTO tax (commodity, name, code, tax_rate)VALUES ('{commodity}', '{name}','{code}', {tax_rate});"
    cursor.execute(sql)
    cursor.close()
    conn.commit()


def query_from_name(commodity):
    cursor = conn.cursor()
    sql = f'select name, code, tax_rate from tax where commodity = "{commodity}"'
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    return values


