import random
import os
import sys
import re
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

class QuestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("问题问答系统 - 鼠标点击版")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 配置样式
        self.setup_styles()
        
        # 初始化变量
        self.questions = []
        self.current_question = ""
        self.current_answer = ""
        self.showing_answer = False
        
        # 创建界面
        self.create_widgets()
        
        # 加载问题文件
        self.load_questions()
        
        # 显示初始问题
        self.show_random_question()
    
    def setup_styles(self):
        """配置界面样式"""
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("微软雅黑", 16))
        style.configure("Question.TLabel", background="#f0f0f0", font=("微软雅黑", 18, "bold"), foreground="#1e3a8a")
        style.configure("Answer.TLabel", background="#f0f0f0", font=("微软雅黑", 16), foreground="#000000")
        style.configure("Instruction.TLabel", background="#f0f0f0", font=("微软雅黑", 14), foreground="#6b7280")
        style.configure("TButton", font=("微软雅黑", 14))
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="问题问答系统", font=("微软雅黑", 18, "bold"))
        title_label.pack(pady=(0, 10))
        
        # 问题显示区域
        self.question_frame = ttk.Frame(main_frame)
        self.question_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 问题标签
        self.question_label = ttk.Label(
            self.question_frame, 
            text="", 
            style="Question.TLabel",
            wraplength=700,
            justify=tk.LEFT
        )
        self.question_label.pack(pady=10)
        
        # 答案标签（初始隐藏）
        self.answer_label = ttk.Label(
            self.question_frame, 
            text="", 
            style="Answer.TLabel",
            wraplength=700,
            justify=tk.LEFT
        )
        self.answer_label.pack(pady=10)
        self.answer_label.pack_forget()  # 初始隐藏
        
        # 指示标签
        self.instruction_label = ttk.Label(
            main_frame, 
            text="点击问题区域显示答案，再次点击显示新问题", 
            style="Instruction.TLabel"
        )
        self.instruction_label.pack(pady=10)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # 加载文件按钮
        load_button = ttk.Button(button_frame, text="选择问题文件", command=self.load_file_dialog)
        load_button.pack(side=tk.LEFT, padx=5)
        
        # 重新加载按钮
        reload_button = ttk.Button(button_frame, text="重新加载", command=self.reload_questions)
        reload_button.pack(side=tk.LEFT, padx=5)
        
        # 绑定点击事件到问题框架
        self.question_frame.bind("<Button-1>", self.on_click)
        self.question_label.bind("<Button-1>", self.on_click)
        self.answer_label.bind("<Button-1>", self.on_click)
        
        # 使标签可获取焦点以便接收点击事件
        self.question_label.config(cursor="hand2")
        self.answer_label.config(cursor="hand2")
        self.question_frame.config(cursor="hand2")
    
    def load_questions(self, file_path="2025SpringAutumn.txt"):
        """读取问题文件并解析成问题列表（支持多行答案）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = []
                for line in f:
                    # 保留原始行内容，但移除行尾换行符
                    stripped_line = line.rstrip('\n')
                    # 跳过空行（包括只包含空格的行）
                    if stripped_line.strip():
                        lines.append(stripped_line)
        except FileNotFoundError:
            messagebox.showerror("错误", f"文件 '{file_path}' 不存在！\n请确保文件在当前目录或选择正确的文件。")
            sys.exit(1)
        except UnicodeDecodeError:
            messagebox.showerror("错误", f"文件 '{file_path}' 编码错误！\n请确保文件保存为UTF-8编码。")
            sys.exit(1)
        
        questions = []
        current_question = None
        current_answer_lines = []
        
        for line in lines:
            # 检查是否是问题行（以数字编号开头，如 "1. "、"2. "、"10."）
            if re.match(r'^\d+\.', line) or re.match(r'^\d+\.\s', line):
                # 保存上一个问题（如果有）
                if current_question is not None:
                    # 如果答案有内容，才保存
                    if current_answer_lines:
                        questions.append((current_question, "\n".join(current_answer_lines)))
                    else:
                        print(f"警告：问题 '{current_question}' 无答案，已跳过")
                # 开始新问题
                current_question = line
                current_answer_lines = []
            else:
                # 收集答案行（包括多行）
                if current_question is not None:
                    current_answer_lines.append(line)
        
        # 处理最后一个题目
        if current_question is not None:
            if current_answer_lines:
                questions.append((current_question, "\n".join(current_answer_lines)))
            else:
                print(f"警告：问题 '{current_question}' 无答案，已跳过")
        
        if not questions:
            messagebox.showerror("错误", "文件中没有有效的问题-答案对！")
            sys.exit(1)
        
        self.questions = questions
        print(f"成功加载 {len(questions)} 个问题（包含多行答案）")
        # messagebox.showinfo("成功", f"成功加载 {len(questions)} 个问题")
    
    def show_random_question(self):
        """显示随机问题"""
        if not self.questions:
            messagebox.showwarning("警告", "没有可用的问题！")
            return
        
        # 随机选择一个问题
        self.current_question, self.current_answer = random.choice(self.questions)
        
        # 更新界面
        self.question_label.config(text=self.current_question)
        self.answer_label.config(text=self.current_answer)
        
        # 隐藏答案，显示问题
        self.showing_answer = False
        self.answer_label.pack_forget()
        self.instruction_label.config(text="点击问题区域显示答案")
    
    def on_click(self, event=None):
        """处理点击事件"""
        if not self.questions:
            return
        
        if self.showing_answer:
            # 如果正在显示答案，点击后显示新问题
            self.show_random_question()
        else:
            # 如果正在显示问题，点击后显示答案
            self.answer_label.pack(pady=10)
            self.showing_answer = True
            self.instruction_label.config(text="再次点击显示新问题")
    
    def load_file_dialog(self):
        """打开文件选择对话框"""
        file_path = filedialog.askopenfilename(
            title="选择问题文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                self.load_questions(file_path)
                self.show_random_question()
            except Exception as e:
                messagebox.showerror("错误", f"加载文件时出错：{str(e)}")
    
    def reload_questions(self):
        """重新加载当前文件"""
        # 尝试重新加载当前文件（这里简单地重新加载默认文件）
        try:
            self.load_questions("2025SpringAutumn.txt")
            self.show_random_question()
        except Exception as e:
            messagebox.showerror("错误", f"重新加载时出错：{str(e)}")

def main():
    root = tk.Tk()
    app = QuestionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
