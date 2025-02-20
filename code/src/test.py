import tkinter as tk

def print_message():
    if running:  # 检查标志变量
        print("每隔 1 秒执行一次")
        root.after(1000, print_message)

def start_task():
    global running
    running = True
    print_message()

def stop_task():
    global running
    running = False

root = tk.Tk()
root.title("定时任务示例")

running = False  # 标志变量

start_button = tk.Button(root, text="开始", command=start_task)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="停止", command=stop_task)
stop_button.pack(pady=10)

root.mainloop()