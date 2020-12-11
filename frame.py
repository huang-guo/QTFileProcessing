import tkinter as tk
from tkinter import ACTIVE, END

from events import *


class Menu(tk.Menu):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.add_command(label="加载商品数据", command=load_commodity_data)
        self.add_command(label="加载链接数据", command=load_link_data)


class FileListbox(tk.Listbox):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack()


class MyBtn(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack(side="left")


class MyFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack()


class MyLabelFrame(tk.LabelFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack(side='left', expand='yes')


class MyTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.load_config()
        self.config(menu=Menu())
        self.file_listbox = FileListbox(master=self, width=100, )
        self.btn_frame1 = MyFrame(self)
        self.add_files_btn = MyBtn(self.btn_frame1,
                                   text="添加文件", command=lambda: add_files(self))
        self.delete_btn = MyBtn(self.btn_frame1,
                                text="删除文件", command=self.delete_file)
        self.delete_all_btn = MyBtn(self.btn_frame1,
                                    text='删除全部文件', command=self.delete_all_files)
        self.btn_frame2 = MyLabelFrame(self, text="请处理")
        self.summary_btn = MyBtn(self.btn_frame2, text="汇总",
                                 command=lambda: self.add_files(summary(self)))
        self.invoice_btn = MyBtn(self.btn_frame2, text="生成发票清单", command=lambda: invoice(self))
        self.add_link_btn = MyBtn(self.btn_frame2, text="添加链接",
                                  command=lambda: add_link(self))

    def load_config(self):
        from settings import FORM_SIZE, TITLE
        self.geometry(FORM_SIZE)
        self.title(TITLE)

    def delete_file(self, index=ACTIVE):
        self.file_listbox.delete(index)

    def add_files(self, files):
        for item in files:
            if item not in self.file_listbox.get(0, END):
                self.file_listbox.insert(END, item)
            else:
                messagebox.showinfo('提示', '文件已经存在')

    def delete_all_files(self):
        self.file_listbox.delete(0, END)

    def get_files(self):
        return self.file_listbox.get(0, END)

    def pop_files(self):
        files = self.file_listbox.get(0, END)
        if files:
            self.file_listbox.delete(0, END)
        return files
