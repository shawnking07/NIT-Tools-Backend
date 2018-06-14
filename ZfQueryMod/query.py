# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from ZfQueryMod.handleAlertMsg import handle_alert_msg


# 查询课表 TODO 单双周解析
def course_table(uid, session, url):
    new_url = url + "xskbcx.aspx?xh=" + uid + "&gnmkdm=N121603"
    headers = {
        'Referer': url + "xs_main.aspx?xh=" + uid
    }
    r = session.get(new_url, headers=headers)
    d = pq(r.text)
    table = d("#Table1 tr:gt(1) td")
    raw_courses = [item.text() for item in table.items() if item.text() != ""]
    return course_format(raw_courses)


def course_str_to_dict(s):
    l = s.split("\n")
    return {'name': l[0], 'time': l[1], 'teacher': l[2], 'location': l[3]}


def course_format(raw):
    Mo = []
    Tu = []
    We = []
    Th = []
    Fr = []
    Sa = []
    Su = []
    for i in raw:
        if "周一" in i:
            Mo.append(course_str_to_dict(i))
            continue
        if "周二" in i:
            Tu.append(course_str_to_dict(i))
            continue
        if "周三" in i:
            We.append(course_str_to_dict(i))
        if "周四" in i:
            Th.append(course_str_to_dict(i))
            continue
        if "周五" in i:
            Fr.append(course_str_to_dict(i))
            continue
        if "周六" in i:
            Sa.append(course_str_to_dict(i))
            continue
        if "周日" in i:
            Su.append(course_str_to_dict(i))
            continue
    course = [Su, Mo, Tu, We, Th, Fr, Sa]
    return course


# 查询历年分数 TODO 选择学期
def query_score(uid, session, url):
    new_url = url + "xscjcx.aspx?xh=" + uid + "&gnmkdm=N121605"
    headers = {
        'Referer': url + "xs_main.aspx?xh=" + uid
    }

    r = session.get(new_url, headers=headers)
    d = pq(r.text)
    view_state = d("input[name='__VIEWSTATE']").val()
    headers['Referer'] = new_url
    payload = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': view_state,
        'hidLanguage': '',
        'btn_zcj': '%C0%FA%C4%EA%B3%C9%BC%A8',
        'ddlXN': '',
        'ddlXQ': '',
        'ddl_kcxz': ''
    }
    r = session.post(new_url, headers=headers, data=payload)
    d = pq(r.text)
    data_list = []
    lines = d("table.datelist tr:gt(0)")
    for i in lines.items():
        retake_flag = False
        if pq(i)("td:eq(14)").text() != "":
            retake_flag = True
        subject_data = {'name': pq(i)("td:eq(3)").text(), 'weight': float(pq(i)("td:eq(6)").text()),
                        'score': pq(i)("td:eq(8)").text(), 'makeUpScore': pq(i)("td:eq(10)").text(),
                        'retake': retake_flag}
        data_list.append(subject_data)
    return data_list


# 查询考试
def query_exam(uid, session, url):
    new_url = url + "xskscx.aspx?xh=" + uid + "&gnmkdm=N121604"
    headers = {
        'Referer': url + "xs_main.aspx?xh=" + uid
    }
    r = session.get(new_url, headers=headers)
    msg = handle_alert_msg(r.text)  # 垃圾提示
    d = pq(r.text)
    # years = [i.text() for i in d("select[name='xnd'] option:gt(0)").items()]  # 垃圾系统自带Bug第一条为空
    exam_table = d("table.datelist tr:gt(0)")
    exams = []
    for i in exam_table.items():
        exam = {'name': pq(i)("td:eq(1)").text(), 'time': pq(i)("td:eq(3)").text(),
                'location': pq(i)("td:eq(4)").text(), 'seat': pq(i)("td:eq(6)").text()}
        exams.append(exam)
    return msg, exams
