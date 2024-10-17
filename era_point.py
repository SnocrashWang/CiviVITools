import tkinter as tk
import json


BUTTON_INFO = [
    {"type": "settlement", "text": "城市人口", "score": 1, "limit": 4},
    {"type": "settlement", "text": "烂地建城", "score": 1, "limit": 5},
    {"type": "settlement", "text": "异大陆建城", "score": 2, "limit": 2},
    {"type": "settlement", "text": "自然奇观建城", "score": 2, "limit": 2},
    {"type": "settlement", "text": "文明附近建城", "score": 1, "limit": 2},
    {"type": "settlement", "text": "多3城市", "score": 3, "limit": 3},
    {"type": "district", "text": "+3学院", "score": 3, "limit": 1},
    {"type": "district", "text": "+3圣地", "score": 3, "limit": 1},
    {"type": "district", "text": "+3剧院", "score": 3, "limit": 1},
    {"type": "district", "text": "+4商业", "score": 3, "limit": 1},
    {"type": "district", "text": "+4港口", "score": 3, "limit": 1},
    {"type": "district", "text": "+4工业", "score": 3, "limit": 1},
    {"type": "improvement", "text": "行业/公司/垄断", "score": 1, "limit": 3},
    {"type": "improvement", "text": "灾害肥沃改良", "score": 1, "limit": 3},
    {"type": "improvement", "text": "特色改良/建筑", "score": 4, "limit": 1},
    {"type": "improvement", "text": "环球航行", "score": 3, "limit": 1},
    {"type": "wonder", "text": "旧时代奇观", "score": 3, "limit": 5},
    {"type": "wonder", "text": "现时代奇观", "score": 4, "limit": 5},
    {"type": "wonder", "text": "招募伟人", "score": 1, "limit": 5},
    {"type": "wonder", "text": "过半费购买伟人", "score": 3, "limit": 3},
    {"type": "civic", "text": "新时代市政", "score": 1, "limit": 1},
    {"type": "civic", "text": "高级政体", "score": 2, "limit": 2},
    {"type": "tech", "text": "新时代科技", "score": 1, "limit": 1},
    {"type": "tech", "text": "船", "score": 2, "limit": 1},
    {"type": "tech", "text": "马", "score": 1, "limit": 1},
    {"type": "tech", "text": "铁", "score": 1, "limit": 1},
    {"type": "tech", "text": "硝石", "score": 1, "limit": 1},
    {"type": "religion", "text": "创立宗教", "score": 2, "limit": 1},
    {"type": "religion", "text": "圆满宗教", "score": 3, "limit": 1},
    {"type": "religion", "text": "宗教审讯", "score": 1, "limit": 1},
    {"type": "religion", "text": "宗教战争皈依", "score": 3, "limit": 3},
    {"type": "religion", "text": "圣城皈依", "score": 4, "limit": 2},
    {"type": "diplomacy", "text": "城邦首个宗主", "score": 2, "limit": 3},
    {"type": "diplomacy", "text": "战争时推翻宗主", "score": 2, "limit": 3},
    {"type": "diplomacy", "text": "征召", "score": 1, "limit": 3},
    {"type": "diplomacy", "text": "敌方附近征召", "score": 2, "limit": 2},
    {"type": "diplomacy", "text": "其他文明贸易站", "score": 1, "limit": 3},
    {"type": "diplomacy", "text": "世界会议获胜", "score": 2, "limit": 5},
    {"type": "military", "text": "特色单位", "score": 4, "limit": 1},
    {"type": "military", "text": "建立军队/舰队", "score": 1, "limit": 4},
    {"type": "military", "text": "单位四级升级", "score": 1, "limit": 3},
    {"type": "military", "text": "城市解放", "score": 2, "limit": 3},
    {"type": "military", "text": "占领首都", "score": 4, "limit": 2},
    {"type": "military", "text": "消灭文明", "score": 5, "limit": 2},
]

red = "#FF3333"
green = "#99FF33"
font = "Consolas"


class CalculatorApp:
    def __init__(self, root, button_info):
        self.total = 0
        self.button_states = {}  # 保存每个按钮的状态
        
        # 设置窗口标题
        root.title("时代分计算器")
        
        # 创建显示框架
        display_frame = tk.Frame(root)
        display_frame.pack(pady=20)
        
        # 创建总和显示框
        self.display = tk.Label(display_frame, text="时代分:  0/31", font=(font, 15))
        self.display.pack(side="left", padx=10)
        
        # 添加重置按钮到总和显示旁边
        reset_button = tk.Button(display_frame, text="重置", font=(font, 10), command=self.reset)
        reset_button.pack(side="left", padx=10)
        
        # 按钮框架（按类型分行显示按钮）
        self.button_frames = {}
        
        # 动态添加按钮，基于传入的button_info
        for idx, info in enumerate(button_info):
            text = info['text']  # 按钮显示文本
            score = info['score']  # 按钮加值
            button_type = info['type']  # 按钮类型，用于分行显示
            limit = info.get('limit', 1)  # 按钮点击次数限制，默认为1
            
            # 创建类型对应的按钮框架，如果不存在则创建一个
            if button_type not in self.button_frames:
                self.button_frames[button_type] = tk.Frame(root)
                self.button_frames[button_type].pack(pady=5, anchor="w")  # 使用anchor="w"实现左对齐
            
            # 初始状态为"关"
            self.button_states[idx] = {'button': None, 'score': score, 'limit': limit, 'count': 0}
            
            # 创建按钮，显示text，点击后切换状态
            button = tk.Button(self.button_frames[button_type], text=f"{text} (0)", font=(font, 10), width=15, 
                               command=lambda i=idx, t=text, l=limit: self.toggle_value(i, t, l), bg=red)
            button.pack(side="left", padx=10)
            
            # 保存按钮控件
            self.button_states[idx]['button'] = button
    
    def toggle_value(self, idx, text, limit):
        score = self.button_states[idx]['score']
        count = self.button_states[idx]['count']
        
        # 更新点击次数
        if count < limit:
            # 如果按钮是关闭的，打开并增加值
            self.total += score
            self.button_states[idx]['button'].config(bg=green)
            self.button_states[idx]['count'] += 1
        else:
            # 超过限制时，恢复按钮为红色，并归零加值
            self.total -= score * limit
            self.button_states[idx]['button'].config(bg=red)
            self.button_states[idx]['count'] = 0  # 重置点击次数

        # 更新按钮上的文本，显示点击次数
        current_count = self.button_states[idx]['count']
        self.button_states[idx]['button'].config(text=f"{text} ({current_count})")

        # 更新显示
        self.display.config(text=f"时代分: {self.total:2}/31")
    
    def reset(self):
        # 重置总和和按钮状态
        self.total = 0
        for idx in self.button_states:
            self.button_states[idx]['active'] = False
            self.button_states[idx]['button'].config(bg=red, state=tk.NORMAL)
            # 重置点击次数
            self.button_states[idx]['count'] = 0
            # 重置按钮文本
            original_text = self.button_states[idx]['button']['text'].split(' ')[0]
            self.button_states[idx]['button'].config(text=f"{original_text} (0)")
        
        # 更新显示
        self.display.config(text="时代分:  0/31")


if __name__ == "__main__":
    root = tk.Tk()
    
    # 创建应用并传递按钮信息
    app = CalculatorApp(root, BUTTON_INFO)
    root.mainloop()