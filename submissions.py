# 这个文件主要是处理爬虫的数据，以及将数据保存到数据库中
from crawler import crawler
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import shutil
from tools.normolize import normalize_code
from tools.tools import read_file_content

class Submission:
    def __init__(self, id_value: str, x_value: float,y_value: float):
        self.id = id_value
        self.x = x_value
        self.y = y_value

    def __str__(self):
        return f"Submission(ID: {self.id},x: {self.x}, y: {self.y})"

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y
        }

# 定义一个函数来检查文件内容是否只包含代码
def contains_only_code(content, non_code_pattern):
    # 使用正则表达式来匹配非代码部分，这里假设非代码部分包括中文
    # 如果需要包括其他符号或语言，可以修改正则表达式
    return non_code_pattern.search(content)

# 清洗数据:遍历目录并处理文件的函数
def process_directory(source_dir, dest_dir, non_code_pattern):
    # 遍历指定目录下的所有文件
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # 检查是否为文件
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    language, code = content.split('\n', 1)
                    normalized_code = normalize_code(language, content)
                    # 检查内容是否只包含代码
                    if contains_only_code(content, non_code_pattern):
                        # 获取目标文件路径
                        language_dir = os.path.join(dest_dir, language)
                        dest_file_path = os.path.join(language_dir, filename)
                        # 将处理后的代码写入目标文件
                        with open(dest_file_path, 'w', encoding='utf-8') as f:
                            f.write(normalized_code)
                        print(f"Processed file: {file_path} -> {dest_file_path}")
                    else:
                        print(f"Skipping non-code file: {file_path}")

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# 清洗数据：爬虫有些数据没有清洗完成（不符合算法格式）
def clean_submissions():
    # 设置源目录和目标目录
    source_dir = 'submissions_correct'
    dest_dir = 'clean_correct'
    language = 'python'  # 假设所有文件都是Python代码，或者根据实际情况修改
    # 使用正则表达式来匹配非代码部分，这里假设非代码部分包括非ASCII字符，但保留空白字符（如空格和制表符）
    non_code_pattern = re.compile(r'[^\x00-\x7F\s]+')
    # 调用函数处理目录
    process_directory(source_dir, dest_dir, non_code_pattern)


# 余弦相似度的计算
def calculate_cosine_similarity(text1, text2):
    vectorizer = CountVectorizer()
    corpus = [text1, text2]
    vectors = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(vectors)
    return round(similarity[0][1], 4)  # 保留小数点后四位

# text1 = "class Solution { public int findChampion(int n, int[][] edges) { int[] degree = new int[n]; for (int[] e : edges) { degree[e[1]]++; } int champion = -1; for (int i = 0; i < n; i++) { if (degree[i] == 0) { if (champion == -1) { champion = i; } else { return -1; } } } return champion; } }"
# text2 = "class Solution { public int findChampion(int n, int[][] edges) { boolean[] st = new boolean[n]; for (int[] edge : edges) { if (!st[edge[1]]) st[edge[1]] = true; } int cnt = 0; int champion = -1; for (int i = 0; i < st.length; i++) { if (st[i] == false) { ++ cnt; champion = i; } } return cnt == 1 ? champion : -1; } }"
# cosine_similarity = calculate_cosine_similarity(text1, text2)
# print(cosine_similarity)

# 找到基准值
def find_java_file_content(directory,language):
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # 检查是否为文件
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    lan = content.split(' ', 1)[0]

                    # 检查第一行是否包含"Java"
                    if language in lan:
                        return content
            except Exception as e:
                print(f"Error reading file {filename}: {e}")

    # 如果没有找到符合条件的文件，返回None或空字符串
    return None

# 计算纵坐标：计算所有正解的余弦相似度
def correct_count(language):
    # 基准值：第一个文件的代码
    target_dir = 'clean_correct'
    language_dir = os.path.join(target_dir, language)
    base = find_java_file_content(language_dir,language)
    if base:
        print(base)
    else:
        print("No file with 'Java' in the first line was found.")
    # 遍历目录下的所有文件 计算其y值 存入元组中
    submissions = []
    for filename in os.listdir(language_dir):
        file_path = os.path.join(language_dir, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    y = calculate_cosine_similarity(base,content)*100
                    submissions.append(Submission(filename,100.0,y))
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    submissions_dicts = [submission.to_dict() for submission in submissions]
    # print("submissions_dicts:")
    # print(submissions_dicts)
    return submissions_dicts

# 找到差值最小的元素
def find_closest_y_value_element(array, target_y):
    min_diff = float('inf')  # 初始化最小差值为正无穷大
    closest_element = None  # 初始化最接近的元素为None

    for element in array:
        y_value = element['y']  # 获取当前元素的y值
        diff = abs(y_value - target_y)  # 计算y值与目标值的差值的绝对值

        if diff < min_diff:  # 如果当前差值小于最小差值
            min_diff = diff  # 更新最小差值
            closest_element = element  # 更新最接近的元素

    return closest_element

# 所有 code 的基准值：clean_correct文件夹中第一个文件的代码
def getBase(language):
    # 基准值：第一个文件的代码
    target_dir = 'clean_correct'
    language_dir = os.path.join(target_dir, language)
    base = find_java_file_content(language_dir, language)
    if base:
        print(base)
        return base
    else:
        print("No file with 'Java' in the first line was found.")


# 错解文件处理
def error_count(language,correct_submission):
    # 基准值：第一个文件的代码
    target_dir = 'clean_correct'
    language_dir = os.path.join(target_dir, language)
    base = find_java_file_content(language_dir, language)
    if base:
        print(base)
    else:
        print("No file with 'Java' in the first line was found.")
    # 遍历目录下的所有文件 计算其y值 存入元组中
    submissions = []
    error_dir = 'submissions_error'
    for filename in os.listdir(error_dir):
        file_path = os.path.join(error_dir, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    y = calculate_cosine_similarity(base, content) * 100
                    solution = find_closest_y_value_element(correct_submission,y)
                    print("solution:"+str(solution))
                    x = calculate_cosine_similarity(read_file_content(solution['id'],language_dir), content) * 100
                    submissions.append(Submission(filename, x, y))
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    submissions_dicts = [submission.to_dict() for submission in submissions]
    return submissions_dicts

# 计算单个提交代码的 x,y 坐标
def xy_count(language,code):
    # 基准值：第一个文件的代码
    target_dir = 'clean_correct'
    language_dir = os.path.join(target_dir, language)
    base = getBase(language)
    y = round(calculate_cosine_similarity(base, code) * 100, 4)
    correct_submission = correct_count(language)
    solution = find_closest_y_value_element(correct_submission, y)
    print("solution:" + str(solution))
    x = round(calculate_cosine_similarity(read_file_content(solution['id'], language_dir), code) * 100, 4)
    return [x,y]


# 删除指定目录
def clear_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # 遍历目录下的所有文件和子目录
        for root, dirs, files in os.walk(directory_path, topdown=False):
            # 遍历子目录下的所有文件并删除
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
                    # 保留子目录，不需要对dirs进行任何操作
        print(f'The contents of {directory_path} have been cleared.')
    else:
        print(f'The directory {directory_path} does not exist or is not a directory.')

def correct_error_count(language):
    correct_submission = correct_count(language)  # 计算纵坐标：计算所有正解的余弦相似度
    error_submission = error_count(language,correct_submission)
    print(error_submission)
    return error_submission


def main():
    # clear_directory('submissions_correct')
    # clear_directory('submissions_error')
    # clear_directory('clean_correct')
    # crawler('find-first-and-last-position-of-element-in-sorted-array')  # 开始爬虫
    # clean_submissions() # 数据清理：清理爬虫后不合规的数据
    # correct_submission = correct_count('cpp')  # 计算纵坐标：计算所有正解的余弦相似度
    # error_submission = error_count('cpp',correct_submission)
    correct_error_count('cpp')


if __name__ == '__main__':
    main()

