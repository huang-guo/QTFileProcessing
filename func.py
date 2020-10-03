import pandas as pd
import tkinter as tk
import os
from tkinter.constants import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames, askopenfilename
import json


def layout(master: tk.Tk):
    master.geometry('500x500')
    master.title('前途文体')

    def load_data():

        file_name = askopenfilename(
            filetypes=[('文本', '.txt')],
        )
        d = {}
        if file_name:
            with open(file_name)as f:
                for line in f.readlines()[3:]:
                    line = line.replace('\n', '')
                    line = line.replace('否', '0').replace('是', '1')
                    a = line.split(',')
                    if len(a[-6] + a[-8]) != 19:
                        continue
                    else:
                        d[a[1]] = [a[4], a[-1], a[-6] + a[-8], eval(a[-5])]
            with open('./commodity.json', 'w', encoding='utf-8') as f2:
                json.dump(d, f2, ensure_ascii=False, indent=4)
            messagebox.showinfo('提示', '导入成功')

    def load_link():
        file_name = askopenfilename(
            filetypes=[('链接', '.xls')],
        )

        if file_name:
            df = get_df(file_name)
            links = df['链接']
            names = df['商品全名'] + df['单价'].astype(str)
            d = dict(zip(names, links))
            if os.access('./link.json', os.F_OK):
                print(1)
                old_links = load_link_json()
                old_links.update(d)
                d = old_links
            with open('./link.json', 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=4)
            messagebox.showinfo('提示', '导入成功')

    menu_bar = tk.Menu(master)
    menu_bar.add_command(label="加载数据", command=load_data)
    menu_bar.add_command(label="加载链接", command=load_link)

    master.config(menu=menu_bar)

    listbox = tk.Listbox(master, width=100)
    listbox.pack()

    def popup():

        file_names = askopenfilenames(
            filetypes=[('excel', '.xls')],
        )
        for item in file_names:
            if item not in listbox.get(0, END):
                listbox.insert(END, item)
            else:
                messagebox.showinfo('提示', '文件已经存在')

    bt_frame = tk.Frame(master)
    bt_frame.pack(side="top")
    popup_btn = tk.Button(bt_frame, text="添加文件", command=popup)
    popup_btn.pack(side="left")

    def delete():
        listbox.delete(0, END)

    delete_btn = tk.Button(bt_frame, text="删除全部", command=delete)
    delete_btn.pack(side="left")
    label_frame = tk.LabelFrame(master, text="请处理")
    label_frame.pack(side='left', expand='yes')

    def summary():
        files = summary_excel(listbox.get(0, END))
        delete()

        for file in files:
            listbox.insert(END, file)

    def invoice():
        generate_excel(listbox.get(0, END))

    def link():
        add_link(listbox.get(0, END))

    summary_btn = tk.Button(label_frame, text="汇总", command=summary)
    summary_btn.pack(side="left")
    invoice_btn = tk.Button(label_frame, text="生成发票清单", command=invoice)
    invoice_btn.pack(side="left")
    link_btn = tk.Button(label_frame, text="添加链接", command=link)
    link_btn.pack(side="left")


def add_link(files):
    d = load_link_json()
    keys = d.keys()
    for file in files:
        try:
            link = []
            df = get_df(file)
            names = df['商品全名'] + df['单价'].astype(str)
            for name in names:
                if name in keys:
                    link.append(d[name])
                else:
                    link.append(None)
            df['链接'] = link
            df.to_excel(file.replace('.xls', '(链接).xls'), index=False)
            messagebox.showinfo('提示', file + '添加链接成功')
        except Exception as e:
            messagebox.showerror(e, file + '添加链接失败')


def summary_excel(files):
    result = []
    for file in files:
        try:
            serif = get_df(file)
            s = serif.groupby(['商品全名', '单位', '单价'], as_index=False)['数量'].sum()
            d = pd.DataFrame(s)
            d['金额'] = d['数量'] * d['单价']
            d.insert(0, '序号', range(1, len(d) + 1), )
            new_file = file.replace('.', '(汇总).')
            d.to_excel(file.replace('.', '(汇总).'), encoding='utf-8', index=False)
            messagebox.showinfo('提示', file + '汇总成功')
            result.append(new_file)
        except Exception as e:
            messagebox.showerror(e, file + '汇总失败')
    return result


def generate_excel(files):
    with open('commodity.json', encoding='utf-8')as f:
        d = json.load(f)
    for file in files:
        try:
            k = 1
            df = pd.read_excel('增值税发票税控开票软件清单信息数据接口规范样例.xls')
            serif = get_df(file)
            err = []
            best = None
            for i in range(1, len(serif) + 1):
                s = serif.loc[i]
                if s['数量'] < 1:
                    continue
                w = s['商品全名']
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
                    l1 = [i, best, s['单位'], None, s['数量'],
                          s['数量'] * s['单价'], d[best][0], None, None,
                          get_s(s['数量'], s['单价'], d[best][0]),
                          None, None, s['单价'], 1, d[best][1], d[best][2],
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


def get_s(num, price, t):
    num = float(num)
    price = float(price)
    t = float(t)
    return round(((num * price) * t) / (1 + t), 2)


def load_link_json():
    with open('./link.json', encoding='utf-8')as f:
        d = json.load(f)
    return d


def get_df(file):
    df = pd.read_excel(file, header=None).dropna()
    df.columns = df.iloc[0]
    df = df[df['商品全名'] != '商品全名']
    df.index = range(1, len(df) + 1)
    return df
