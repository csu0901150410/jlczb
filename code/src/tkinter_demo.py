import tkinter as tk
from tkinter import messagebox

import threading

from pyjlccam import *

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("jlcCAM Plugin")
        self.root.geometry("800x600")

        self.jlccam = JlccamClient("127.0.0.1", 4066)

        # 初始化界面组件
        self.create_top_buttons()
        self.create_bottom_listbox()

        self.check_open_jobs()

    def create_top_buttons(self):
        """创建顶部按钮"""
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # 创建按钮
        button1 = tk.Button(top_frame, text="打开料号", command=self.on_button1_click)
        button1.pack(side=tk.LEFT, padx=5, pady=5)

        button2 = tk.Button(top_frame, text="关闭料号", command=self.on_button2_click)
        button2.pack(side=tk.LEFT, padx=5, pady=5)

    def create_bottom_listbox(self):
        """创建底部列表框和滚动条"""
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # 创建滚动条
        scrollbar = tk.Scrollbar(bottom_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建列表框
        self.listbox = tk.Listbox(bottom_frame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 将滚动条与列表框关联
        scrollbar.config(command=self.listbox.yview)

        # 添加示例数据
        self.add_sample_data()

    def add_sample_data(self):
        """向列表框中添加示例数据"""
        jobs = self.jlccam.get_job_list()
        for jobname in jobs:
            self.listbox.insert(tk.END, jobname)

    def on_button1_click(self):
        if not self.listbox.curselection():
            messagebox.showwarning("提示", "请选择料号再尝试打开!")
            return

        jobname = self.listbox.get(self.listbox.curselection())
        self.jlccam.open_job(jobname)

        self.listbox.itemconfig(self.listbox.curselection(), bg="green")
    def on_button2_click(self):
        if not self.listbox.curselection():
            messagebox.showwarning("提示", "请选择料号再尝试关闭!")
            return
        
        jobname = self.listbox.get(self.listbox.curselection())
        
        if not self.jlccam.check_job_open(jobname):
            messagebox.showwarning("提示", "料号未打开!")
            return
        
        jobinfo = self.jlccam.get_jobinfo_by_jobname(jobname)
        job = JlccamJob("127.0.0.1", jobinfo.port)
        job.close()

        self.listbox.itemconfig(self.listbox.curselection(), bg="white")


    # 循环检测打开的料号，将列表中打开的料号底色改为绿色
    def check_open_jobs(self):
        jobs = self.jlccam.get_all_open_jobinfo()
        for job in jobs:
            for i in range(self.listbox.size()):
                if self.listbox.get(i) == job.jobname:
                    self.listbox.itemconfig(i, bg="green")
                    break
                else:
                    self.listbox.itemconfig(i, bg="white")
        self.root.after(10000, self.check_open_jobs)

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()