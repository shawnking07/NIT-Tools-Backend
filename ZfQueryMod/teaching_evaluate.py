import urllib.parse
import re
from pyquery import PyQuery as pq


def get_teaching_evaluate_urls(uid, name, session, url):
    new_url = url + "xsjxpj2.aspx?xh=" + uid + "&xm=" + urllib.parse.quote(str(name).encode('gb2312')) + "&gnmkdm=N123205"
    headers = {
        'Referer': url + "xs_main.aspx?xh=" + uid
    }
    r = session.get(new_url, headers=headers)
    d = pq(r.text)
    links = d("table .datelist td:gt(0) a")
    dt_urls = []
    for item in links.items():
        attr = item.attr("onclick")
        url = attr[13:-92]
        dt_urls.append(url)
    return dt_urls

def evaluate(uid, name, session, base_url):
    urls = get_teaching_evaluate_urls(uid, name, session, base_url)
    headers = {
        'Referer': base_url + "xs_main.aspx?xh=" + uid
    }
    for url in urls:
        r = session.get(base_url + url, headers=headers)
        d = pq(r.text)
        view_state = d("input[name='__VIEWSTATE']").val()
        payload = {
            '__VIEWSTATE': view_state,
            'Datagrid1:_ctl2:rb': 95,
            'Datagrid1:_ctl3:rb': 95,
            'Datagrid1:_ctl4:rb': 95,
            'Datagrid1:_ctl5:rb': 95,
            'Datagrid1:_ctl6:rb': 95,
            'Datagrid1:_ctl7:rb': 95,
            'txt_pjxx': '',
            'Button1': '+%CC%E1+%BD%BB+'
        }
        headers = {
            'Referer': base_url + url
        }
        r = session.post(base_url + url, headers=headers, data=payload)

    new_url = base_url + "xsjxpj2.aspx?xh=" + uid + "&xm=" + urllib.parse.quote(str(name).encode('gb2312')) + "&gnmkdm=N123205"
    headers = {
        'Referer': base_url + "xs_main.aspx?xh=" + uid
    }
    r = session.get(new_url, headers=headers)
    d = pq(r.text)
    view_state = d("input[name='__VIEWSTATE']").val()
    payload = {
        '__EVENTTARGET': "",
        '__EVENTARGUMENT': "",
        '__VIEWSTATE': view_state,
        'btn_tj': '+%CC%E1+%BD%BB+'
    }
    headers = {
        'Referer': new_url
    }
    r = session.post(new_url, headers=headers, data=payload)
