from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from submissions import correct_count, correct_error_count
from tools.tools import read_file_content

app = Flask(__name__)
# 数据库连接
uri = 'mysql+pymysql://root:root@127.0.0.1:3306/CodeProgressVis'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.String(255), primary_key=True)
    x = db.Column(db.Float)
    y = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y
        }


# 新增函数，用于添加元素到数据库中
def add_submissions_to_db(submissions_list):
    with app.app_context():  # 确保在app上下文中工作
        for submission_dict in submissions_list:
            submission = Submission(
                id=submission_dict['id'],
                x=submission_dict['x'],
                y=submission_dict.get('y', None)  # 如果'y'不存在，则为None
            )
            db.session.add(submission)
        db.session.commit()  # 提交所有变更到数据库


# 获取全部的Submissions
def getSubmissions():
    # submissions_list = correct_error_count('cpp')
    # add_submissions_to_db(submissions_list)
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
    content = read_file_content(id, 'submissions_error')
    if (content == None):
        content = read_file_content(id, 'submissions_correct')
    return jsonify(content)


if __name__ == '__main__':
    app.run()
