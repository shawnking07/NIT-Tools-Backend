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
    # print(name[:-2])
    return str(name[:-2]), session


def s_login(username, password, url, max_times):
    i = 0
    while i < max_times:
        try:
            i += 1
            return login(username, password, url)
        except Exception:
            pass
        time.sleep(2)
    # print("用户名或密码错误")
    raise Exception("Login Error")
