import sqlite3

conn = sqlite3.connect("./src/data.db")


def create():
    cursor = conn.cursor()
    sql = "create table if not exists link(" \
          "id INTEGER PRIMARY KEY," \
          "'name' varchar(30) not null ," \
          "url varchar(60) not null ," \
          "price float not null);"
    cursor.execute(sql)
    cursor.close()
    conn.commit()


def insert(name, price, url):
    cursor = conn.cursor()
    sql = f"INSERT INTO link (name, url, price)VALUES ('{name}', '{url}', {price});"
    cursor.execute(sql)
    cursor.close()
    conn.commit()


def query_from_name(name):
    cursor = conn.cursor()
    sql = f'select id,price,url from link where name = "{name}"'
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    return values


def query_from_name_and_price(name, price):
    cursor = conn.cursor()
    sql = f'select id,price,url from link where name = "{name}" and price = {price}'
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    return values


def update_from_id(pk, url):
    cursor = conn.cursor()
    sql = f'update link set url="{url}" where id={pk} ;'
    cursor.execute(sql)
    cursor.close()
    conn.commit()