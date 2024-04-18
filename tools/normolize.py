# 这个文件专用于根据语言规范化代码
import re

def normalize_java_code(code):
    # 删除单行和多行注释
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/*.*?\*/', '', code, flags=re.DOTALL)

    # 删除print调用（如果需要）
    code = re.sub(r'\bSystem\.out\.println\s*\(.*?\);', '', code)

    # 删除额外间距和换行符
    code = re.sub(r'\s+', ' ', code)

    return code


def normalize_python_code(code):

    # 删除单行注释
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)

    # 删除print调用
    code = re.sub(r'\bprint\s*\(.*?\);', '', code)

    # 删除额外间距和换行符
    code = re.sub(r'\s+', ' ', code)

    return code


def normalize_c_or_cpp_code(code):
    # 删除单行和多行注释
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'/*.*?\*/', '', code, flags=re.DOTALL)

    # 对于C和C++，这里不删除输出函数，因为它们有多种形式（例如printf, cout等）
    # 如果需要，请添加相应的正则表达式
    # 删除额外间距和换行符
    code = re.sub(r'\s+', ' ', code)

    return code


def normalize_code(language, code):
    if language == 'java':
        return normalize_java_code(code)
    elif language == 'python':
        return normalize_python_code(code)
    elif language in ['c', 'cpp']:
        return normalize_c_or_cpp_code(code)
    else:
        raise ValueError(f"Unsupported language: {language}")


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    input_file_path = 'public/data01.txt'
    output_file_path = 'public/output.txt'

    # 读取文件内容
    content = read_file(input_file_path)

    # 分割语言和代码
    language, code = content.split('\n', 1)

    # 规范化代码
    normalized_code = normalize_code(language, code)

    # 写入规范化后的代码到文件
    write_file(output_file_path, normalized_code)


if __name__ == '__main__':
    main()