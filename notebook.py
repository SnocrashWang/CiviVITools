import tkinter as tk
from tkinter import ttk

from era_point import ERA_POINT_INFO, EraPointApp
from discount import DISTRICT_INFO, DiscountApp


def create_notebook(root):
    notebook = ttk.Notebook(root)  # 创建 Notebook
    notebook.pack(expand=True, fill='both')

    # 创建第一个标签页，包含 CounterApp
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="时代分计算器")
    EraPointApp(tab1, ERA_POINT_INFO)

    # 创建第二个标签页，包含 AnotherApp
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="半价区域计算器")
    DiscountApp(tab2, DISTRICT_INFO)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("今天踹飞了吗")

    # 创建包含两个标签页的 Notebook
    create_notebook(root)

    root.mainloop()