import json
import os
import pandas as pd

from settings import FIELD_COMMODITY, FIELD_NUM, FIELD_PRICE, FIELD_UNIT


def get_amount_tax(num, price, t):
    num = float(num)
    price = float(price)
    t = float(t)
    return round(((num * price) * t) / (1 + t), 2)


def get_df(file):
    df = pd.read_excel(file, header=None).dropna()
    df.columns = df.iloc[0]
    for field in [FIELD_COMMODITY, FIELD_NUM, FIELD_PRICE, FIELD_UNIT]:
        if field not in df.columns:
            raise ValueError('字段错误')
    df = df[df[FIELD_COMMODITY] != FIELD_COMMODITY]
    df.index = range(1, len(df) + 1)
    return df


def fix_wins_file_bug(content):
    if content.startswith(u'\ufeff'):
        content = content.encode('utf8')[3:].decode('utf8')
    return content


def load_json_from_file(file_name):
    if os.access(file_name, os.F_OK):
        file = open(file_name, encoding='utf-8')
        data = json.loads(fix_wins_file_bug(file.read()))
        file.close()
        if data:
            return data
        else:
            return {}
    else:
        return {}


def dump_json_to_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
