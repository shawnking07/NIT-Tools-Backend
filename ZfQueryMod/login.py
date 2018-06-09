# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
from PIL import Image
from io import BytesIO
from ZfQueryMod.CAPTCHA_decode import load_predict
import time


# 登陆正方获取姓名和关键公告
def login(username, password, url):
    r = requests.get(url)
    session = requests.session()
    d = pq(r.text)
    # print(d.html())
    view_state = d("input[name='__VIEWSTATE']").val()
    r_code = session.get(url + "CheckCode.aspx")
    im = Image.open(BytesIO(r_code.content))
    # im.show()
    # secret_code = input("input the secret code: ")
    secret_code = load_predict(im)
    payload = {
        '__VIEWSTATE': view_state,
        'txtUserName': username,
        'Textbox1': "",
        'TextBox2': password,
        'txtSecretCode': secret_code,
        'RadioButtonList1': "%D1%A7%C9%FA",
        'Button1': ""
    }
    r = session.post(url + "default2.aspx", data=payload)
    d = pq(r.text)
    name = d("#xhxm").html()
    from ZfQueryMod.handleAlertMsg import handle_alert_msg
    board_msg = handle_alert_msg(r.text)[0]
    if name is not None:
        return 0, session, name[:-2], board_msg
    else:
        msg = handle_alert_msg(r.text)[0]
        if "验证码" in msg:
            return 1, msg
        elif "密码" in msg:
            return 2, msg
        elif "用户名" in msg:
            return 3, msg


# 循环登陆以解决部分验证码识别错误的问题
def s_login(username, password, url, max_times=4):
    i = 0
    while i < max_times:
        i += 1
        lg = login(username, password, url)
        if lg[0] == 0:
            return lg[1], lg[2], lg[3]
        elif lg[0] == 1:
            time.sleep(1)
        elif lg[0] == 2:
            raise Exception(lg[1])
        elif lg[0] == 3:
            raise Exception(lg[1])
    raise Exception("验证码识别错误")
