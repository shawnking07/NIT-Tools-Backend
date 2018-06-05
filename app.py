from flask import Flask
from flask import request
from flask import make_response, Response
from flask import session
from ZfQueryMod.login import s_login
from APIException import *
import os
app = Flask(__name__)


app.secret_key = os.urandom(24)
url = "http://10.80.96.131/"


def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# @app.before_request
# def isLogin():
#     if 'stuId' in session:
#         return True
#     else:
#         return False


@app.errorhandler(APIException)
def handle_api_exception(error):
    from flask import jsonify
    response = jsonify(error.to_dict())
    response.status_code = error.code
    return response


@app.route("/api/login", methods=['GET'])
def login():
    stu_id = request.values.get('stuId')
    password = request.values.get('password')
    try:
        name = s_login(stu_id, password, url, 3)[0]
    except Exception as e:
        print(e)
        raise APIException("ZLE", "ZfSystem Login Error", 401)
    return name


@app.route("/api/history_scores", methods=['GET'])
def history_scores():
    stu_id = request.values.get('stuId')
    password = request.values.get('password')
    try:
        name, zf_session = s_login(stu_id, password, url, 3)
    except Exception as e:
        print(e)
        raise APIException("ZLE", "ZfSystem Login Error", 401)
    from ZfQueryMod.query_score import query_score
    from ZfQueryMod.gpa import average
    scores_list = query_score(stu_id, name, zf_session, url)
    data = {
        "scores": scores_list,
        "avg": average(scores_list)
    }
    raise APIException("ossas", data, 200)


@app.route("/api/course_table", methods=['GET'])
def get_course_table():
    stu_id = request.values.get('stuId')
    password = request.values.get('password')
    try:
        name, zf_session = s_login(stu_id, password, url, 3)
    except Exception as e:
        print(e)
        raise APIException("ZLE", "ZfSystem Login Error", 401)
    from ZfQueryMod.course_table import course_table
    table = course_table(stu_id, name, zf_session, url)
    raise APIException("ossas", table, 200)


@app.route("/api/teaching_evaluate", methods=['GET'])
def teaching_evaluate():
    stu_id = request.values.get('stuId')
    password = request.values.get('password')
    try:
        name, zf_session = s_login(stu_id, password, url, 3)
    except Exception as e:
        print(e)
        raise APIException("oh no", "不知道什么错误", 401)
    from ZfQueryMod.teaching_evaluate import evaluate
    evaluate(stu_id, name, zf_session, url)
    raise APIException("ossas", "成功", 200)
