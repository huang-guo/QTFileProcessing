from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askopenfilenames
from func import *
from doc_process import DocProcess
from settings import COMMODITY_CODE_JS, EXCEL_SUFFIX, FIELD_LINK, LINK_JS


def summary(tk):
    files = tk.pop_files()
    if not files:
        return
    for file in files:
        try:
            yield DocProcess(file).summary()
        except Exception as e:
            messagebox.showerror('错误', file + '\n' + str(e))
            yield file


def load_commodity_data():
    file_name = askopenfilename(
        filetypes=[('文本', '.txt')],
    )
    commodity = {}
    if file_name:
        with open(file_name)as file:
            for line in file.readlines()[3:]:
                line = line.replace('\n', '')
                line = line.replace('否', '0').replace('是', '1')
                a = line.split(',')
                a[-6] += ('0' * (19 - len(a[-6])))

                commodity[a[1]] = [a[4], a[-1], a[-6], eval(a[-5])]
        dump_json_to_file(COMMODITY_CODE_JS, commodity)
        messagebox.showinfo('提示', '导入成功')


def load_link_data():
    file_name = askopenfilename(
        filetypes=[(FIELD_LINK, EXCEL_SUFFIX)],
    )

    if file_name:
        df = get_df(file_name)
        links = df[FIELD_LINK]
        names = df[FIELD_COMMODITY] + df[FIELD_PRICE].astype(str)
        new_links_data = dict(zip(names, links))
        old_links_data = load_json_from_file(LINK_JS)
        if old_links_data:
            new_links_data = old_links_data.update(new_links_data)
        dump_json_to_file(LINK_JS, new_links_data)
        messagebox.showinfo('提示', '导入成功')


def add_files(tk):
    file_names = askopenfilenames(
        filetypes=[('excel', EXCEL_SUFFIX)],
    )
    tk.add_files(file_names)


def add_link(tk):
    files = tk.pop_files()
    if not files:
        return
    link_data = load_json_from_file(LINK_JS)
    for file in files:
        try:
            os.startfile(DocProcess(file).add_links(link_data))
        except Exception as e:
            messagebox.showerror('错误', file + '\n' + str(e))


def invoice(tk):
    files = tk.pop_files()
    if not files:
        return
    commodity_data = load_json_from_file(COMMODITY_CODE_JS)
    for file in files:
        try:
            os.startfile(DocProcess(file).generator_invoice(commodity_data))
        except Exception as e:
            messagebox.showerror('错误', file + '\n' + str(e))
