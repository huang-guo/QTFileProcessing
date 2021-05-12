import tkinter
from tkinter.filedialog import askopenfilename

from file_op.excel_op import get_links
from file_op.json_op import load_commodity_data
from settings import EXCEL_SUFFIX
from .base import FileSelectBox, FileProcessComponent


class MyForm(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.load_config()
        self.menu = tkinter.Menu()
        self.menu.add_command(label="加载商品数据",
                              command=lambda: load_commodity_data(askopenfilename(filetypes=[('商品编码', '.txt')])))
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
