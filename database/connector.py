class Base:
    def __init__(self, conn, table):
        self.conn = conn
        self.table = table

    def create(self):
        pass

    def _insert(self, replace=False, **kwargs):
        cursor = self.conn.cursor()
        columns = ""
        values = ""
        for k in kwargs.keys():
            columns += (k + ',')
            values += f" '{kwargs[k]}' ,"
        columns = columns[:-1]
        values = values[:-1]
        keyword = "replace" if replace else "INSERT"
        sql = f"{keyword} INTO {self.table} ({columns})VALUES ({values});"
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()

    def _query(self, select="*", **kwargs):
        cursor = self.conn.cursor()
        values = ""
        for k in kwargs.keys():
            values += f" {k} = '{kwargs[k]}' and"
        values = values[:-3]
        cursor.execute(f"select {select} from {self.table} where {values}")
        values = cursor.fetchall()
        cursor.close()
        return values

    def _update(self, pk_name, pk, **kwargs):
        cursor = self.conn.cursor()
        values = ""
        for k in kwargs.keys():
            values += f"{k} = '{kwargs[k]}',"
        values = values[:-1]
        cursor.execute(f"update {self.table} set {values} where {pk_name}={pk} ;")
        cursor.close()
        self.conn.commit()


class Link(Base):
    def __init__(self, conn):
        super().__init__(conn, 'link')

    def create(self):
        cursor = self.conn.cursor()
        sql = "create table if not exists link(" \
              "id INTEGER PRIMARY KEY," \
              "'name' varchar(30) not null ," \
              "url varchar(60) not null ," \
              "price float not null);"
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()

    def insert(self, name, price, url):
        super()._insert(name=name, price=price, url=url)

    def query_from_name(self, name):
        return super()._query(select="id,price,url", name=name)

    def query_from_name_and_price(self, name, price):
        return super()._query(select="id,price,url", name=name, price=price)

    def update_url(self, pk, url):
        super()._update("id", pk, url=url)


class Tax(Base):
    def __init__(self, conn):
        super().__init__(conn, 'tax')

    def create(self):
        cursor = self.conn.cursor()
        sql = "create table if not exists tax(" \
              "id INTEGER PRIMARY KEY," \
              "commodity varchar(30) unique," \
              "'name' varchar(15) not null ," \
              "code char(19) not null);"
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()

    def insert(self, commodity, name, code: str):
        code = code.ljust(19, '0')
        super()._insert(replace=True, commodity=commodity, name=name, code=code)

    def query_from_name(self, commodity):
        return super()._query(select="name, code", commodity=commodity)
