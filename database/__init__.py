
from .connector import Link, Tax
import sqlite3

conn = sqlite3.connect("./src/data.db")
links = Link(conn)
tax = Tax(conn)


def create_all():
    links.create()
    tax.create()


__all__ = [links, tax]
