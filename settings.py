import configparser

conf = configparser.ConfigParser()
conf.read('./app.ini', encoding="utf-8")

TITLE = conf.get('FORM', 'title')
FORM_SIZE = conf.get('FORM', 'size')
FIELD_LINK = conf.get('FIELD', 'link')
FIELD_COMMODITY = conf.get('FIELD', 'commodity')
FIELD_PRICE = conf.get('FIELD', 'price')
FIELD_UNIT = conf.get('FIELD', 'unit')
FIELD_NUM = conf.get('FIELD', 'count')
FIELD_MONEY = conf.get('FIELD', 'money')
FIELD_NUMBER = conf.get('FIELD', 'index')
EXCEL_SUFFIX = conf.get('SUFFIX', 'excel').split(',')
