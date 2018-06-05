from login import s_login
from query_score import query_score
# from gpa import average
import sys
import json


url = "http://10.80.96.131/"


if __name__ == '__main__':
    uid = sys.argv[1]
    password = sys.argv[2]
    name, session = s_login(uid, password, url, 3)
    data_list = query_score(uid, name, session, url)
    # average(data_list)
    json_data = {'stuId':uid,'stuName':name,'scores':data_list}
    print(json.dumps(json_data, ensure_ascii=False))
    

