import re
import os

# 根据文件名称返回文件内容
def read_file_content(filename, directory='.'):
    # 构建完整的文件路径，如果filename已经是完整路径，则保持不变
    file_path = os.path.join(directory, filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return None
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误: {e}")
        return None
