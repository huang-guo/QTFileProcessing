import os

import pandas as pd
from pandas import DataFrame

from database import links
from file_op.json_op import load_json_from_file
from settings import FIELD_NUM, FIELD_PRICE, FIELD_UNIT, FIELD_COMMODITY, FIELD_NUMBER, FIELD_MONEY, FIELD_LINK


def get_df(file, fields):
    df = pd.read_excel(file, header=None).dropna()
    df.index = range(len(df))
    df.columns = df.iloc[0]
    df = df.drop(0)
    for field in fields:
        if field not in df.columns:
            raise ValueError(f'字段{field}未发现')
    return df


def summary(file_name):
    if not file_name:
        return
    df = pd.DataFrame(
        get_df(file_name, [FIELD_COMMODITY, FIELD_UNIT, FIELD_PRICE, FIELD_NUM]).groupby(
            [FIELD_COMMODITY, FIELD_UNIT, FIELD_PRICE],
            as_index=False
        )[FIELD_NUM].sum())
    df = df[df[FIELD_NUM].astype(float) > 0]
    df[FIELD_MONEY] = df[FIELD_NUM] * df[FIELD_PRICE]
    df.insert(0, FIELD_NUMBER, range(1, len(df) + 1), )
    path = file_name[:-5] + file_name[-5:].replace('.', '(汇总).')
    df.to_excel(path, encoding='utf-8', index=False)
    return path


def get_links(file_name):
    if not file_name:
        return
    df = get_df(file_name, [FIELD_COMMODITY, FIELD_PRICE, FIELD_LINK])
    for i in df.index:
        loc = df.loc[i]
        query = links.query_from_name_and_price(loc[FIELD_COMMODITY], loc[FIELD_PRICE])
        if not query:
            links.insert(loc[FIELD_COMMODITY], loc[FIELD_PRICE], loc[FIELD_LINK])
        elif query[0][2] != loc[FIELD_LINK]:
            links.update_from_id(query[0][0], loc[FIELD_LINK])


def add_links(file_name):
    if not file_name:
        return
    df = get_df(file_name, [FIELD_COMMODITY, FIELD_PRICE, FIELD_NUM])
    new = []
    none = []
    for i in df.index:
        loc = df.loc[i]
        query = links.query_from_name(loc[FIELD_COMMODITY])
        found = False
        for data in query:
            if data[1] == loc[FIELD_PRICE]:
                loc[FIELD_LINK] = data[2]
                new.append(loc)
                found = True
                break
            elif str(loc[FIELD_PRICE] / data[1])[-1] == '0':
                loc[FIELD_LINK] = data[2]
                loc[FIELD_NUM] *= (loc[FIELD_PRICE] / data[1])
                loc[FIELD_PRICE] = data[1]
                new.append(loc)
                found = True
                break

        if not found:
            none.append(i)
    new_path = file_name[:-5] + file_name[-5:].replace('.', '(链接).')
    none_path = file_name[:-5] + file_name[-5:].replace('.', '(无).')
    DataFrame(new).to_excel(new_path, encoding='utf-8', index=False)
    df.loc[none].to_excel(none_path, encoding='utf-8', index=False)
    os.startfile(none_path)


def generator_invoice(file_name):
    if not file_name:
        return
    k = 1
    commodity_data = load_json_from_file('./src/tax.json')
    df = get_df(file_name, [FIELD_NUM, FIELD_COMMODITY, FIELD_UNIT, FIELD_PRICE])
    mode_df = pd.read_excel('./src/model.xls')
    err = []
    best = None
    for row in df.itertuples():
        num = getattr(row, FIELD_NUM)
        name = getattr(row, FIELD_COMMODITY)
        unit = getattr(row, FIELD_UNIT)
        price = getattr(row, FIELD_PRICE)
        if num <= 0:
            err.append(k)
            continue
        length = 0
        for word in commodity_data.keys():
            if word == name:
                best = word
                length = 1
                break
            elif word in name and len(word) > length:
                length = len(word)
                best = word
        if length != 0:
            line = [
                k, best, unit, None, num,
                num * price, commodity_data[best][0], None, None,
                get_amount_tax(num, price, commodity_data[best][0]),
                None, None, price, 1, commodity_data[best][1],
                commodity_data[best][2], None, commodity_data[best][3], None, None, 0
            ]
            mode_df.loc[k] = line
        else:
            err.append(k)
        k += 1
    mode_df.to_excel(
        file_name[:-5] + file_name[-5:].replace('.', '(发票).'),
        encoding='utf-8', index=False
    )

    err_df = pd.DataFrame(df.loc[err])
    path = file_name[:-5] + file_name[-5:].replace('.', '(无).')
    err_df.to_excel(path, encoding='utf-8', index=False)
    os.startfile(path)


def get_amount_tax(num, price, t):
    num = float(num)
    price = float(price)
    t = float(t)
    return round(((num * price) * t) / (1 + t), 2)
