import random
import os
import sys
import re

def read_questions(file_path):
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
        print(f"错误：文件 '{file_path}' 不存在！")
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
        print("错误：文件中没有有效的问题-答案对！")
        sys.exit(1)
    
    print(f"成功加载 {len(questions)} 个问题（包含多行答案）")
    return questions

def wait_for_key():
    """跨平台等待任意键按下"""
    if os.name == 'nt':  # Windows
        import msvcrt
        msvcrt.getch()
    else:  # Linux/macOS
        import sys, termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    # 文件路径（根据实际文件路径修改）
    file_path = "2025SpringAutumn.txt"  # 请确保文件在当前目录
    
    # 读取问题
    questions = read_questions(file_path)
    
    print("\n" + "="*50)
    print("欢迎使用问题问答系统！")
    print("随机显示一个问题，按任意键查看答案（答案可能有多行）")
    print("="*50 + "\n")
    
    while True:
        # 随机选择一个问题
        question, answer = random.choice(questions)
        
        # 显示问题
        print("问题：", question)
        print("\n请按任意键查看答案... ", end="", flush=True)
        
        # 等待按键
        input()
        
        # 显示答案（保留多行格式）
        print("\n答案：")
        print(answer)
        print("\n" + "-"*50 + "\n")

        print("\n请按任意键刷新下一题... ", end="", flush=True)
        # 等待按键
        input()
        

if __name__ == "__main__":
    main()
