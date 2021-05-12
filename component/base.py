import tkinter as tk
from tkinter import MULTIPLE, ACTIVE, END, messagebox
from tkinter.filedialog import askopenfilenames, askopenfilename
import file_op
from file_op.excel_op import get_links
from file_op.json_op import load_commodity_data
from settings import EXCEL_SUFFIX


class FileSelectBox(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.list_box = tk.Listbox(self, selectmode=MULTIPLE)
        self.add_files_btn = tk.Button(self,
                                       text="添加文件", command=self.add_files)
        self.delete_btn = tk.Button(self,
                                    text="取消文件", command=lambda: self.list_box.delete(ACTIVE))
        self.delete_all_btn = tk.Button(self,
                                        text='取消全部文件', command=lambda: self.list_box.delete(0, END))

    def add_files(self):
        files = askopenfilenames(
            filetypes=[('excel', EXCEL_SUFFIX)],
        )
        if files:
            self.add_files_to_list(files)

    def add_files_to_list(self, files):
        for item in files:
            if item not in self.list_box.get(0, END):
                self.list_box.insert(END, item)

    def get_files(self):
        return self.list_box.get(0, END)

    def pop_files(self):
        files = self.get_files()
        if files:
            self.list_box.delete(0, END)
        return files

    def pack(self):
        self.list_box.pack(fill='x')
        self.add_files_btn.pack(side="left")
        self.delete_btn.pack(side="right")
        self.delete_all_btn.pack(side="right")
        super(FileSelectBox, self).pack(fill="x")


class FileProcessComponent(tk.LabelFrame):
    def __init__(self, master, **kw):
        super().__init__(master, text="请处理", **kw)
        self.master = master
        self.summary_btn = tk.Button(self, text="汇总",
                                     command=self.summaries)
        self.invoice_btn = tk.Button(self, text="生成发票清单", command=self.invoice)
        self.add_link_btn = tk.Button(self, text="添加链接",
                                      command=self.add_links)

    def summaries(self):
        out = []
        for file in self.master.file_select_box.pop_files():
            try:
                out.append(file_op.summary(file))
            except Exception as e:
                messagebox.showerror('错误', file + '\n' + str(e))
                out.append(file)
        self.master.file_select_box.add_files_to_list(out)

    def invoice(self):
        out = []
        for file in self.master.file_select_box.pop_files():
            try:
                file_op.generator_invoice(file)
            except Exception as e:
                messagebox.showerror('错误', file + '\n' + str(e))
                out.append(file)
        if out:
            self.master.file_select_box.add_files_to_list(out)

    def add_links(self):
        out = []
        for file in self.master.file_select_box.pop_files():
            try:
                file_op.add_links(file)
            except Exception as e:
                messagebox.showerror('错误', file + '\n' + str(e))
                out.append(file)
        if out:
            self.master.file_select_box.add_files_to_list(out)

    def pack(self):
        self.summary_btn.pack(side="left")
        self.invoice_btn.pack(side="left")
        self.add_link_btn.pack(side="left")
        super(FileProcessComponent, self).pack(pady=90, side="bottom")
