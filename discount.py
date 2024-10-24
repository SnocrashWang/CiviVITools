import ttkbootstrap as ttk


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
FONT = "Consolas"


class DiscountApp:
    def __init__(self, root, options):
        self.root = root
        self.state = {}  # 存储各选项
        self.unlock = {option['name']: False for option in options}  # 存储各选项的打开/关闭状态
        self.built = {option['name']: 0 for option in options}  # 存储 built 计数
        self.foundation = {option['name']: 0 for option in options}  # 存储 foundation 计数

        # 设置最小长宽，保持窗口大小不变
        for i in range(8):
            root.grid_columnconfigure(i, minsize=80)
        for i in range(7):
            root.grid_rowconfigure(i, minsize=40)
        root.grid_columnconfigure(0, minsize=120)
        root.grid_columnconfigure(3, minsize=120)
        root.grid_columnconfigure(4, minsize=120)
        root.grid_columnconfigure(7, minsize=120)

        col_1 = ttk.Label(root, text="建成数量", width=10)
        col_1.grid(row=0, column=1, padx=20, pady=10)
        col_2 = ttk.Label(root, text="地基数量", width=10)
        col_2.grid(row=0, column=2, padx=20, pady=10)
        col_5 = ttk.Label(root, text="建成数量", width=10)
        col_5.grid(row=0, column=5, padx=20, pady=10)
        col_6 = ttk.Label(root, text="地基数量", width=10)
        col_6.grid(row=0, column=6, padx=20, pady=10)

        # 布局界面
        for idx, option in enumerate(options):
            name = option['name']
            row = idx % int(len(options) / 2) + 1
            col_offset = idx // int(len(options) / 2) * 4

            # 使用 Checkbutton 代替 Button
            name_button = ttk.Checkbutton(root, text=name, bootstyle="success-round-toggle", command=lambda name=name: self.toggle_state(name))
            name_button.grid(row=row, column=0 + col_offset, padx=(40, 10), pady=20, sticky="w")

            spinbox_built = ttk.Spinbox(root, from_=0, to=100, width=5, command=self.update_all_state)
            spinbox_built.grid(row=row, column=1 + col_offset, padx=10, pady=10)
            spinbox_built.set(0)  # 设置初始值为 0

            spinbox_foundation = ttk.Spinbox(root, from_=0, to=100, width=5, command=self.update_all_state)
            spinbox_foundation.grid(row=row, column=2 + col_offset, padx=10, pady=10)
            spinbox_foundation.set(0)  # 设置初始值为 0

            discount_label = ttk.Label(root)
            discount_label.grid(row=row, column=3 + col_offset, padx=(10, 40), pady=10)

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
        self.state[name]['built_spinbox'].set(0)  # 隐藏后将计数设置为 0
        self.state[name]['foundation_spinbox'].grid_remove()
        self.state[name]['foundation_spinbox'].set(0)  # 隐藏后将计数设置为 0
        self.state[name]['label'].grid_remove()

    # 显示 spinbox 和 label
    def show_widgets(self, name):
        self.state[name]['built_spinbox'].grid()
        self.state[name]['foundation_spinbox'].grid()
        self.state[name]['label'].grid()

    # 切换状态（打开/关闭）
    def toggle_state(self, name):
        self.unlock[name] = not self.unlock[name]

        if self.unlock[name]:
            self.show_widgets(name)  # 显示控件
        else:
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
            if flag:
                self.state[name]['label'].config(text="半价", bootstyle="success")
            else:
                self.state[name]['label'].config(text="原价", bootstyle="warning")



if __name__ == "__main__":
    root = ttk.Window()  # 使用 ttk.Window() 创建窗口
    root.title("半价区域计算器")

    # 样式
    style = ttk.Style("superhero")  # 使用solar主题

    app = DiscountApp(root, DISTRICT_INFO)
    root.mainloop()