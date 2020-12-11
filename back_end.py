import os
import pandas as pd

from settings import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


def load_data():
    file_name = askopenfilename(
        filetypes=[('文本', '.txt')],
    )
    commodity = {}


def summary(files):
    result = []
    for file in files:
        try:
            serif = get_df(file)
            s = serif.groupby([FIELD_COMMODITY, FIELD_UNIT, FIELD_PRICE], as_index=False)[FIELD_NUM].sum()
            df = pd.DataFrame(s)
            df[FIELD_MONEY] = df[FIELD_NUM] * df[FIELD_PRICE]
            df.insert(0, FIELD_NUMBER, range(1, len(df) + 1), )
            new_file = file.replace('.', '(汇总).')
            df.to_excel(file.replace('.', '(汇总).'), encoding='utf-8', index=False)
            messagebox.showinfo('汇总成功', file)
            result.append(new_file)
        except Exception as e:
            messagebox.showerror(e, file + '汇总失败')
    return result


def add_link(files):
    links = load_link_json()
    keys = links.keys()
    for file in files:
        try:
            link = []
            df = get_df(file)
            names = df[FIELD_COMMODITY] + df[FIELD_PRICE].astype(str)
            for name in names:
                if name in keys:
                    link.append(links[name])
                else:
                    link.append(None)
            df[FIELD_LINK] = link
            df.to_excel(file.replace('.xls', '(链接).xls'), index=False)
            messagebox.showinfo('提示', file + '添加链接成功')
            os.startfile(file.replace('.xls', '(链接).xls'))
        except Exception as e:
            messagebox.showerror(e, file + '添加链接失败')


def invoice(files):
    with open(COMMODITY_CODE_JS, encoding='utf-8')as f1:
        d = json.load(f1)
    for file in files:
        try:
            k = 1
            df = pd.read_excel(SAMPLE_INVOICE)
            serif = get_df(file)
            err = []
            best = None
            for i in range(1, len(serif) + 1):
                s = serif.loc[i]
                if s[FIELD_NUM] <= 0:
                    err.append(i)
                    continue
                w = s[FIELD_COMMODITY]
                length = 0
                for word in d.keys():
                    if word in w:
                        if word == w:
                            best = word
                            length = 1
                            break
                        elif len(word) > length:
                            length = len(word)
                            best = word
                if length != 0:
                    l1 = [i, best, s[FIELD_UNIT], None, s[FIELD_NUM],
                          s[FIELD_NUM] * s[FIELD_PRICE], d[best][0], None, None,
                          get_s(s[FIELD_NUM], s[FIELD_PRICE], d[best][0]),
                          None, None, s[FIELD_PRICE], 1, d[best][1], d[best][2],
                          None, d[best][3], None, None, 0
                          ]
                    df.loc[k] = l1
                    k += 1
                else:
                    err.append(i)
            new_serif = serif.loc[err]
            err_df = pd.DataFrame(new_serif, )
            err_df.to_excel(file.replace('.xls', '(无).xls'), encoding='utf-8', index=False)
            df.to_excel(file.replace('.xls', '(发票).xls'), encoding='utf-8', index=False)
            messagebox.showinfo('提示', file + '  发票清单成功')

        except Exception as e:

            messagebox.showerror(e, file + '  发票清单错误')
        else:
            os.startfile(file.replace('.xls', '(无).xls'))


def get_s(num, price, t):
    num = float(num)
    price = float(price)
    t = float(t)
    return round(((num * price) * t) / (1 + t), 2)


def load_link_json():
    with open(LINK_JS, encoding='utf-8')as file:
        content = file.read()
    if content.startswith(u'\ufeff'):
        content = content.encode('utf8')[3:].decode('utf8')
    d = json.loads(content)
    return d


def get_df(file):
    df = pd.read_excel(file, header=None).dropna()
    df.columns = df.iloc[0]
    df = df[df[FIELD_COMMODITY] != FIELD_COMMODITY]
    df.index = range(1, len(df) + 1)
    df[FIELD_MONEY] = df[FIELD_PRICE] * df[FIELD_NUM]
    return df
