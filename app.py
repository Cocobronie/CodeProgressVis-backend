import os
import shutil
import uuid

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import random
from submissions import correct_count, correct_error_count, find_java_file_content, getBase, xy_count
from tools.tools import read_file_content

app = Flask(__name__)
# 数据库连接
uri = 'mysql+pymysql://root:root@127.0.0.1:3306/CodeProgressVis?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.String(255), primary_key=True)
    sId = db.Column(db.Integer)
    sName = db.Column(db.String(255))
    x = db.Column(db.Float)
    y = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'sId': self.sId,
            'sName': self.sName,
            'x': self.x,
            'y': self.y
        }

# 用于删除学生单次提交代码
def delete_submissions_from_folder(folder_path):
    # 获取当前应用的上下文
    with app.app_context():
        # 遍历文件夹
        for filename in os.listdir(folder_path):
            # 假设文件名只包含ID（例如：123.py）
            try:
                submission_id = filename
                # 在数据库中查询记录
                submission = Submission.query.get(submission_id)
                if submission:
                    # 如果找到记录，则删除它
                    db.session.delete(submission)
                    db.session.commit()
                    print(f"Deleted submission with ID: {submission_id}")
                    # 删除对应的文件
                    file_path = os.path.join(folder_path, filename)
                    os.unlink(file_path)
                    print(f"Deleted file {file_path}")
                else:
                    print(f"No submission found with ID: {submission_id}")
            except (ValueError, FileNotFoundError, OSError) as e:
                # 处理文件名不是整数、文件不存在或其他文件系统错误
                print(f"Error while processing file {filename}: {e}")

# 新增函数，用于添加元素到数据库中
def add_submissions_to_db(submissions_list):
    with app.app_context():  # 确保在app上下文中工作
        for submission_dict in submissions_list:
            submission = Submission(
                id=submission_dict['id'],
                sId=random.randint(1, 10),
                sName='张三',
                x=submission_dict['x'],
                y=submission_dict.get('y', None)  # 如果'y'不存在，则为None
            )
            db.session.add(submission)
        db.session.commit()  # 提交所有变更到数据库


# 将用户新提交的代码相关的信息存储到数据库中
def add_new_to_db(submission):
    with app.app_context():  # 确保在app上下文中工作
        db.session.add(submission)
        db.session.commit()  # 提交所有变更到数据库


# 根据id查询sId
def get_sid_by_id(submission_id):
    # 假设 submission_id 是您想要查询的 id 值
    # 使用 SQLAlchemy 的 session 来查询数据库
    submission = Submission.query.filter_by(id=submission_id).first()
    if submission:
        # 如果找到了匹配的记录，返回
        return submission
    else:
        # 如果没有找到匹配的记录，返回 None 或其他适当的值
        return None

# 根据sId查询submissions
def get_ids_by_sId(sId):
    # 使用 SQLAlchemy 的 session 来查询数据库
    # 注意：这里我们使用 filter 而不是 filter_by，因为 filter_by 不支持非等值比较
    submissions = Submission.query.filter_by(sId = sId).all()
    submissions_dicts = [submission.to_dict() for submission in submissions]
    print("submissions")
    print(submissions_dicts)
    if submissions_dicts:
        # 如果找到了匹配的记录，返回 id 列表
        return submissions_dicts
    else:
        # 如果没有找到匹配的记录，返回空列表或其他适当的值
        return []

    # 获取全部的Submissions
def getSubmissions():
    # 下面的四行代码只需要运行一次：作用将爬虫计算的数据存储到数据库，不过只用存储一次
    # submissions_list_correct = correct_count('cpp')
    # add_submissions_to_db(submissions_list_correct)
    # submissions_list_error = correct_error_count('cpp')
    # add_submissions_to_db(submissions_list_error)

    submissions = Submission.query.all()
    submissions_dicts = [submission.to_dict() for submission in submissions]
    for s in submissions_dicts:
        print(s)
    return jsonify(submissions_dicts)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/login/outLogin', methods=['POST'])
def outLogin():
    data = {"data": '{}', "success": 'true'}
    return jsonify(data)


@app.route('/api/currentUser')
def currentUser():
    data = {
        "success": 'true',
        "data": {
            "name": "Serati Ma",
            "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png",
            "userid": "00000001",
            "email": "antdesign@alipay.com",
            "signature": "海纳百川，有容乃大",
            "title": "交互专家",
            "group": "蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED",
            "tags": [
                {
                    "key": "0",
                    "label": "很有想法的"
                },
                {
                    "key": "1",
                    "label": "专注设计"
                },
                {
                    "key": "2",
                    "label": "辣~"
                },
                {
                    "key": "3",
                    "label": "大长腿"
                },
                {
                    "key": "4",
                    "label": "川妹子"
                },
                {
                    "key": "5",
                    "label": "海纳百川"
                }
            ],
            "notifyCount": 12,
            "unreadCount": 11,
            "country": "China",
            "access": "admin",
            "geographic": {
                "province": {
                    "label": "浙江省",
                    "key": "330000"
                },
                "city": {
                    "label": "杭州市",
                    "key": "330100"
                }
            },
            "address": "西湖区工专路 77 号",
            "phone": "0752-268888888"
        }
    }
    return jsonify(data)


@app.route('/api/login/account', methods=['POST'])
def login():
    data = {
        'status': 'ok',
        'type': 'account',
        'currentAuthority': 'admin',
    }
    return jsonify(data)


@app.route('/api/submissions')
def submissions():
    return getSubmissions()


@app.route('/api/code')
def submissionsByid():
    id = request.args.get('id')  # 获取名为 'id' 的查询参数
    # filename = 'dataset/{id}.txt'.format(id=id)  # 替换为你的文件名
    # 从数据库中查询学生ID
    submission = get_sid_by_id(id)
    print(submission)
    content = read_file_content(id, 'submissions_error')
    if (content == None):
        content = read_file_content(id, 'submissions_correct')
    if (content == None):
        content = read_file_content(id, 'submissions_stu')
    if(content == None):
        data = {
            'status': 'error'
        }
        print(data)
        return jsonify(data)
    else:
        data = {
            'status': 'ok',
            'sId': submission.sId,
            'sName': submission.sName,
            'content': content
        }
        print(data)
        return jsonify(data)


# 根据学生ID查找他提交的代码列表
@app.route('/api/search')
def searchesByid():
    id = request.args.get('id')  # 获取名为 'id' 的查询参数
    # 从数据库中查询学生ID对应的提交
    submissions = get_ids_by_sId(id)
    content_list = []
    for s in submissions:
        print(s)
        id = s['id']
        content = read_file_content(id, 'submissions_error')
        if (content == None):
            content = read_file_content(id, 'submissions_correct')
        if (content == None):
            content = read_file_content(id, 'submissions_stu')
        if (content != None):
            content_list.append(content)
    if(content_list == []):
        data = {
            'status': 'error'
        }
        print(data)
        return jsonify(data)
    else:
        data = {
            'status': 'ok',
            'submissions':submissions,
            'sId': submissions[0]['sId'],
            'sName': submissions[0]['sName'],
            'content_list': content_list
        }
        print(data)
        return jsonify(data)

# 接受学生提交的代码，并且计算出横纵坐标值，存储到数据库并且返回给前端坐标
@app.route('/api/submit', methods=['POST'])
def submitCode():
    code = request.args.get('code')
    sName = request.args.get('sName')
    sId = request.args.get('sId')

    point = xy_count('cpp', code)
    print('code' + code)

    # 将代码写入文件夹
    filename = uuid.uuid1()
    with open('submissions_stu/{}.txt'.format(filename), 'w', encoding='utf') as f:
        f.write(code)
    id = str(filename) + '.txt'

    # 将横纵坐标添加到数据库中
    add_new_to_db(Submission(
        id=id,
        sId=sId,
        sName=sName,
        x=point[0],
        y=point[1]
    ))

    data = {
        'id': id,
        'status': 'ok',
        'x_Field': point[0],
        'y_Field': point[1]
    }
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
    # delete_submissions_from_folder('submissions_stu') # 清理文件夹submissions_stu/