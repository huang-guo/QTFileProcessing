import tkinter as tk

from back_end import *
from tkinter.constants import END
from tkinter.filedialog import askopenfilenames


def layout(master: tk.Tk):
    master.geometry('500x500')
    master.title('前途文体')

    menu_bar = tk.Menu(master)
    menu_bar.add_command(label="加载数据", command=load_data)
    menu_bar.add_command(label="加载链接", command=load_link)

    master.config(menu=menu_bar)

    listbox = tk.Listbox(master, width=100)
    listbox.pack()

    bt_frame = tk.Frame(master)
    bt_frame.pack(side="top")

    def popup():
        file_names = askopenfilenames(
            filetypes=[('excel', EXCEL_SUFFIX)],
        )
        for item in file_names:
            if item not in listbox.get(0, END):
                listbox.insert(END, item)
            else:
                messagebox.showinfo('提示', '文件已经存在')

    popup_btn = tk.Button(bt_frame, text="添加文件", command=popup)
    popup_btn.pack(side="left")

    delete_btn = tk.Button(bt_frame, text="删除全部",
                           command=lambda: listbox.delete(0, END))
    delete_btn.pack(side="left")
    label_frame = tk.LabelFrame(master, text="请处理")
    label_frame.pack(side='left', expand='yes')

    summary_btn = tk.Button(label_frame, text="汇总",
                            command=lambda: summary(listbox.get(0, END)))
    summary_btn.pack(side="left")

    invoice_btn = tk.Button(label_frame, text="生成发票清单",
                            command=lambda: invoice(listbox.get(0, END)))
    invoice_btn.pack(side="left")
    link_btn = tk.Button(label_frame, text="添加链接",
                         command=lambda: add_link(listbox.get(0, END)))
    link_btn.pack(side="left")
