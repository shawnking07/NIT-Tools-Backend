from pyquery import PyQuery as pq
import re


def handle_alert_msg(html):
    d = pq(html)
    scripts = d("script")
    msgs = []
    for i in scripts.items():
        script = i.text()
        if "alert" in script:
            s = re.match(r"alert\('(.*)'\)", script).group(0)
            msgs.append(s[7:-2])
    return msgs