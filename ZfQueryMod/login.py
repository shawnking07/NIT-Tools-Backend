import requests
from pyquery import PyQuery as pq
from PIL import Image
from io import BytesIO
from ZfQueryMod.CAPTCHA_decode import load_predict
import time



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
    # print(r.text)
    d = pq(r.text)
    name = d("#xhxm").html()
    if name != None:
        return 0, name[:-2], session
    else:
        from ZfQueryMod.handleAlertMsg import handle_alert_msg
        msgs = handle_alert_msg(r.text)
        if "验证码" in msgs[0]:
            return 1, msgs[0]
        elif "密码" in msgs[0]:
            return 2, msgs[0]
        elif "用户名" in msgs[0]:
            return 3, msgs[0]


def s_login(username, password, url, max_times=4):
    i = 0
    while i < max_times:
        i += 1
        lg = login(username, password, url)
        if lg[0] == 0:
            return lg[1], lg[2]
        elif lg[0] == 1:
            time.sleep(1)
        elif lg[0] == 2:
            raise Exception("密码错误")
        elif lg[0] == 3:
            raise Exception("学号错误或未按照要求参加教学活动")
    raise Exception("验证码识别错误")
