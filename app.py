# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask import make_response
from flask import request
from flask import jsonify

from APIException import *
from ZfQueryMod.login import s_login

app = Flask(__name__)


app.secret_key = os.urandom(24)
url = "http://10.80.96.131/"


# 解决跨域
@app.after_request
def response_headers(content):
    resp = make_response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.code
    return response


@app.route("/api/login", methods=['POST'])
def login():
    stu_id = request.get_json()['stuId']
    password = request.get_json()['password']
    try:
        zf_session, name, board_msg = s_login(stu_id, password, url)
    except Exception as e:
        print(e)
        raise APIException("error", str(e), 401)
    return jsonify({'name': name, 'board_msg': board_msg})


@app.route("/api/history_scores", methods=['POST'])
def history_scores():
    stu_id = request.get_json()['stuId']
    password = request.get_json()['password']
    try:
        zf_session, name, board_msg = s_login(stu_id, password, url)
    except Exception as e:
        print(e)
        raise APIException("error", str(e), 401)
    from ZfQueryMod.query import query_score
    from ZfQueryMod.gpa import average
    scores_list = query_score(stu_id, zf_session, url)
    if not scores_list:
        raise APIException("oops", "未进行教学评价", 403)
    data = {
        "scores": scores_list,
        "avg": average(scores_list)
    }
    return jsonify(data)


@app.route("/api/course_table", methods=['POST'])
def get_course_table():
    stu_id = request.get_json()['stuId']
    password = request.get_json()['password']
    try:
        zf_session, name, board_msg = s_login(stu_id, password, url)
    except Exception as e:
        print(e)
        raise APIException("error", str(e), 403)
    from ZfQueryMod.query import course_table
    table = course_table(stu_id, zf_session, url)
    raise jsonify(table)


@app.route("/api/teaching_evaluate", methods=['POST'])
def teaching_evaluate():
    stu_id = request.get_json()['stuId']
    password = request.get_json()['password']
    try:
        zf_session, name, board_msg = s_login(stu_id, password, url)
    except Exception as e:
        print(e)
        raise APIException("error", str(e), 403)
    from ZfQueryMod.teaching_evaluate import evaluate
    evaluate(stu_id, zf_session, url)
    return "ossas"
