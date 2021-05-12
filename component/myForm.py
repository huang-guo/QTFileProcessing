import tkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askopenfilenames

from file_op.excel_op import get_links, load_commodity_data_to_db
from file_op.json_op import load_commodity_data
from settings import EXCEL_SUFFIX
from .base import FileSelectBox, FileProcessComponent


class MyForm(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.load_config()
        self.menu = tkinter.Menu()
        self.menu.add_command(label="加载商品数据",
                              command=self.load_commodity_from_txt)
        self.menu.add_command(label="加载商品数据（excel)",
                              command=self.load_commodity_from_excel)
        self.menu.add_command(label="加载链接数据",
                              command=lambda: get_links(askopenfilename(filetypes=[('excel', EXCEL_SUFFIX)], )))
        self.config(menu=self.menu)
        self.file_select_box = FileSelectBox(self)
        self.file_select_box.pack()
        self.file_process_component = FileProcessComponent(self)
        self.file_process_component.pack()

    def load_config(self):
        from settings import FORM_SIZE, TITLE
        self.geometry(FORM_SIZE)
        self.title(TITLE)

    @staticmethod
    def load_commodity_from_excel():
        files = askopenfilenames(
            filetypes=[('excel', EXCEL_SUFFIX)],
        )
        if files:
            for file in files:
                try:
                    load_commodity_data_to_db(file)

                except Exception as e:
                    messagebox.showerror('错误', file + '\n' + str(e))

    @staticmethod
    def load_commodity_from_txt():
        file = askopenfilename(filetypes=[('商品编码', '.txt')])
        if file:
            try:
                load_commodity_data(file)
            except Exception as e:
                messagebox.showerror('错误', str(e))

    @staticmethod
    def load_link_from_excel():
        files = askopenfilenames(
            filetypes=[('excel', EXCEL_SUFFIX)],
        )
        if files:
            for file in files:
                try:
                    get_links(file)
                except Exception as e:
                    messagebox.showerror('错误', file + '\n' + str(e))
