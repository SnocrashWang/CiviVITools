import tkinter as tk
from tkinter import ttk

# 样例数据
DISTRICT_INFO = [
    {"name": "港口"},
    {"name": "圣地"},
    {"name": "学院"},
    {"name": "商业"},
    {"name": "军营"},
    {"name": "工业"},
    
    {"name": "市政"},
    {"name": "娱乐"},
    {"name": "剧院"},
    {"name": "外交"},
    {"name": "保护区"},
    {"name": "航空港"}
]

RED = "#FF3333"
GREEN = "#99FF33"
FONT = "Consolas"


class DiscountApp:
    def __init__(self, root, options):
        self.root = root
        self.state = {}  # 存储各选项
        self.unlock = {option['name']: False for option in options}  # 存储各选项的打开/关闭状态，False 为关闭，True 为打开
        self.built = {option['name']: 0 for option in options}  # 存储 built 计数
        self.foundation = {option['name']: 0 for option in options}  # 存储 foundation 计数
        
        # 自定义样式
        style = ttk.Style()
        style.configure("TSpinbox", arrowwidth=20, font=(FONT, 10))

        # 设置最小宽度，保持窗口大小不变
        root.grid_columnconfigure(1, minsize=80)  # built_spinbox 所在列
        root.grid_columnconfigure(2, minsize=80)  # foundation_spinbox 所在列
        root.grid_columnconfigure(3, minsize=80)  # discount_label 所在列
        root.grid_columnconfigure(5, minsize=80)  # built_spinbox 所在列
        root.grid_columnconfigure(6, minsize=80)  # foundation_spinbox 所在列
        root.grid_columnconfigure(7, minsize=80)  # discount_label 所在列

        col_1 = tk.Label(root)
        col_1.config(text="建成数量", width=10)
        col_1.grid(row=0, column=1, padx=10, pady=5)
        col_2 = tk.Label(root)
        col_2.config(text="地基数量", width=10)
        col_2.grid(row=0, column=2, padx=10, pady=5)
        col_5 = tk.Label(root)
        col_5.config(text="建成数量", width=10)
        col_5.grid(row=0, column=5, padx=10, pady=5)
        col_6 = tk.Label(root)
        col_6.config(text="地基数量", width=10)
        col_6.grid(row=0, column=6, padx=10, pady=5)
        
        # 布局界面
        for idx, option in enumerate(options):
            name = option['name']
            
            # 计算每个控件所在的行和列
            # row = idx // 2  # 每两个选项一行
            # col_offset = (idx % 2) * 4  # 计算列偏移量，偶数列偏移 0，奇数列偏移 4
            
            row = idx % int(len(options) / 2) + 1
            col_offset = idx // int(len(options) / 2) * 4
            
            # 使用按钮代替 Label 显示名称，按下时切换状态
            name_button = tk.Button(root, text=name, bg=RED, width=15, command=lambda name=name: self.toggle_state(name))
            name_button.grid(row=row, column=0 + col_offset, padx=10, pady=5)
            
            # 使用 ttk.Spinbox 控件，增减按钮的样式更大
            spinbox_built = ttk.Spinbox(root, from_=0, to=100, width=5, style="TSpinbox", command=self.update_all_state)
            spinbox_built.grid(row=row, column=1 + col_offset, padx=5)
            spinbox_built.set(0)  # 设置初始值为 0

            spinbox_foundation = ttk.Spinbox(root, from_=0, to=100, width=5, style="TSpinbox", command=self.update_all_state)
            spinbox_foundation.grid(row=row, column=2 + col_offset, padx=5)
            spinbox_foundation.set(0)  # 设置初始值为 0
            
            # discount label
            discount_label = tk.Label(root)
            discount_label.grid(row=row, column=3 + col_offset, padx=10, pady=5)
            
            # 存储每个选项对应的控件和状态
            self.state[name] = {
                'name_button': name_button,
                'built_spinbox': spinbox_built,
                'foundation_spinbox': spinbox_foundation,
                'label': discount_label
            }

            # 初始时隐藏 spinbox 和 label
            self.hide_widgets(name)

    # 隐藏 spinbox 和 label
    def hide_widgets(self, name):
        self.state[name]['built_spinbox'].grid_remove()
        self.state[name]['built_spinbox'].set(0)                # 隐藏后将计数设置为 0
        self.state[name]['foundation_spinbox'].grid_remove()
        self.state[name]['foundation_spinbox'].set(0)           # 隐藏后将计数设置为 0
        self.state[name]['label'].grid_remove()

    # 显示 spinbox 和 label
    def show_widgets(self, name):
        self.state[name]['built_spinbox'].grid()
        self.state[name]['foundation_spinbox'].grid()
        self.state[name]['label'].grid()

    # 切换状态（打开/关闭）
    def toggle_state(self, name):
        # 切换状态 True/False
        self.unlock[name] = not self.unlock[name]
        
        # 根据状态改变按钮颜色和文本
        if self.unlock[name]:
            self.state[name]['name_button'].config(bg=GREEN)
            self.show_widgets(name)  # 显示控件
        else:
            self.state[name]['name_button'].config(bg=RED)
            self.hide_widgets(name)  # 隐藏控件

        self.update_all_state()

    # 计算是否半价
    def judge_discount(self, name, unlock, built_all):
        if built_all < unlock:
            return False
        if self.built[name] + self.foundation[name] >= built_all / max(unlock, 1):
            return False
        return True

    # 更新所有选项的计数和差异显示
    def update_all_state(self):
        # 刷新计数
        for name in self.state:
            self.built[name] = int(self.state[name]['built_spinbox'].get())
            self.foundation[name] = int(self.state[name]['foundation_spinbox'].get())

        unlock = sum(v for v in self.unlock.values())
        built_all = sum(n for n in self.built.values())
        for name in self.state:
            flag = self.judge_discount(name, unlock, built_all)
            text = "半价" if flag else "原价"
            self.state[name]['label'].config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("半价区域计算器")
    
    # 创建应用并传递按钮信息
    app = DiscountApp(root, DISTRICT_INFO)
    root.mainloop()