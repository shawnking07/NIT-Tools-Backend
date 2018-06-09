# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import re


# 正方系统过于垃圾使用alert进行消息提示
# 该函数用于alert解析
def handle_alert_msg(html):
    d = pq(html)
    scripts = d("script")
    msgs = []
    for i in scripts.items():
        script = i.text()
        if "alert" in script:
            s = re.match(r"alert\('(.*?)'\)", script).group(0)
            msgs.append(s[7:-2])
    return msgs
