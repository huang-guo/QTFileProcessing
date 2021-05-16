import tkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askopenfilenames

from file_op.excel_op import get_links, load_commodity_data_to_db
from file_op.json_op import load_commodity_data
from settings import Config
from .base import FileSelectBox, FileProcessComponent


class MyForm(tkinter.Tk):
    _setting = Config('FORM')

    def __init__(self):
        super().__init__()
        self.load_config()
        self.menu = tkinter.Menu()
        self.menu.add_command(label="加载商品数据",
                              command=self.load_commodity_from_txt)
        self.menu.add_command(label="加载商品数据（excel)",
                              command=self.load_commodity_from_excel)
        self.menu.add_command(label="加载链接数据",
                              command=self.load_link_from_excel)
        self.config(menu=self.menu)
        self.file_select_box = FileSelectBox(self)
        self.file_select_box.pack()
        self.file_process_component = FileProcessComponent(self)
        self.file_process_component.pack()

    def load_config(self):
        self.geometry(self._setting.get('size'))
        self.title(self._setting.get('title'))

    @staticmethod
    def load_commodity_from_excel():
        files = askopenfilenames(
            filetypes=[('excel', ['.xls', '.xlsx'])],
        )
        if files:
            for file in files:
                try:
                    load_commodity_data_to_db(file)
                    messagebox.showinfo('提示', '导入成功')
                except Exception as e:
                    messagebox.showerror('错误', file + '\n' + str(e))

    @staticmethod
    def load_commodity_from_txt():
        file = askopenfilename(filetypes=[('商品编码', '.txt')])
        if file:
            try:
                load_commodity_data(file)
                messagebox.showinfo('提示', '导入成功')
            except Exception as e:
                messagebox.showerror('错误', str(e))

    @staticmethod
    def load_link_from_excel():
        files = askopenfilenames(
            filetypes=[('excel', ['.xls', '.xlsx'])],
        )
        if files:
            for file in files:
                try:
                    get_links(file)
                    messagebox.showinfo('提示', '导入成功')
                except Exception as e:
                    messagebox.showerror('错误', file + '\n' + str(e))
