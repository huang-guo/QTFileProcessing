import tkinter
import windnd

from tkinter import ttk
from tkinter.constants import *


class BaseFrame:
    def __init__(self, context=None):
        self.context = context
        self.tk = tkinter.Tk()
        self.tk.wm_attributes('-topmost', 1)
        self.on_create()
        self.tk.mainloop()
        self.control = []

    def on_create(self):
        self.tk.geometry("300x300")

    def on_destroy(self):
        self.tk.destroy()

    def start_frame(self, frame_name: type, context={}):
        self.on_destroy()
        frame_name(context)


class FileDrop(BaseFrame):
    def on_create(self):
        super().on_create()
        windnd.hook_dropfiles(self.tk, self.dropped_files)
        label = tkinter.Label(self.tk, text="将要进行操作的文件移进来")
        label.pack()

    def dropped_files(self, files):
        file_list = []
        for item in files:
            file_list.append(item.decode('gbk'))
        self.start_frame(FileSelect, context={"file_list": file_list})


class FileSelect(BaseFrame):
    def on_create(self):
        super().on_create()
        text_list = tkinter.Listbox(self.tk)
        text_list.pack(fill="x")
        for file in self.context['file_list']:
            text_list.insert(END, file)
        choices = tkinter.StringVar()
        method = ttk.Combobox(self.tk, textvariable=choices, text="方法")
        method["values"] = ('给文件添加链接', '处理方法2', '处理方法3')
        method["state"] = "readonly"
        method.pack()

        def process_method(*args):
            self.context['method'] = method.get()

        method.bind('<<ComboboxSelected>>', func=process_method)

        bottom_btn_box = tkinter.LabelFrame(self.tk)
        bottom_btn_box.pack(expand="yes")
        define_btn = tkinter.Button(bottom_btn_box, text="确定")
        define_btn.pack(side="left")
        define_btn.bind('<Button-1>', func=self.define)
        back_btn = tkinter.Button(bottom_btn_box, text="返回")
        back_btn.pack(side="left")
        back_btn.bind('<Button-1>', func=self.back)

    def define(self, event):
        pass

    def back(self, *args):
        self.start_frame(FileDrop)
