# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from ZfQueryMod.handleAlertMsg import handle_alert_msg


# 查询课表
def course_table(uid, session, url):
    new_url = url + "xskbcx.aspx?xh=" + uid + "&gnmkdm=N121603"
    headers = {
        'Referer': url + "xs_main.aspx?xh=" + uid
    }
    r = session.get(new_url, headers=headers)
    d = pq(r.text)
    table = d("#Table1 tr:gt(1)")
    tds = pq(table)("td:gt(1)")
    courses = []
    for item in tds.items():
        if item.text() != "":
            courses.append(item.text())
    return courses


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
