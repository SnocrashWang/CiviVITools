from ttkbootstrap import Style, Window, Frame, Notebook

from era_point import ERA_POINT_INFO, EraPointApp
from discount import DISTRICT_INFO, DiscountApp

def create_notebook(root):
    style = Style(theme='superhero')  # 使用 superhero 主题
    
    notebook = Notebook(root, bootstyle='primary')  # 创建 Notebook
    notebook.pack(expand=True, fill='both')

    # 创建第一个标签页，包含 EraPointApp
    tab1 = Frame(notebook, padding=10)
    notebook.add(tab1, text='时代分计算器')
    EraPointApp(tab1, ERA_POINT_INFO)

    # 创建第二个标签页，包含 DiscountApp
    tab2 = Frame(notebook, padding=10)
    notebook.add(tab2, text='半价区域计算器')
    DiscountApp(tab2, DISTRICT_INFO)

if __name__ == "__main__":
    root = Window()  # 创建窗口并设置主题
    root.title("今天踹飞了吗")

    # 创建包含两个标签页的 Notebook
    create_notebook(root)

    root.mainloop()