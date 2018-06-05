import urllib.parse
from pyquery import PyQuery as pq


def course_table(uid, name, session, url):
    new_url = url + "xskbcx.aspx?xh=" + uid + "&xm=" + urllib.parse.quote(str(name).encode('gb2312')) + "&gnmkdm=N121603"
    headers = {
        'Referer': url + "xs_main.aspx?xh=" + uid
    }
    r = session.get(new_url, headers=headers)
    d = pq(r.text)
    table = d("#Table1 tr:gt(1)")
    tds = pq(table)("td:gt(1)")
    courses = []
    for item in tds.items():
        if (item.text() != ""):
            courses.append(item.text())
    return courses