import requests
from requests import cookies
import os
import json

DATA_DIR = 'destination'
BASE_URL = 'https://ddl.wustacm.top'
my_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
}
client = requests.session()
client.headers.update(my_headers)
client.cookies.set_cookie(
    cookie=cookies.create_cookie("sessionid", ""))


def init_cookies():
    client.get(BASE_URL + '/api/problem/')
    client.cookies.get('csrftoken')
    client.headers.update({
        'x-csrftoken': client.cookies.get('csrftoken'),
        'Accept': 'application/json'
    })


# 返回manifest
def upload_test_cases(file_path):
    res = client.post(BASE_URL + '/api/problem/upload_test_cases/', data={
        "spj": False,
    }, files={

        "file": open(file_path, 'rb')
    })
    return res.text


def post_problem_desc(description):
    res = client.post(BASE_URL + '/api/problem/', json=description)
    print(res.text)
    res_json = json.loads(res.text)
    return res_json['err'] is None


def import_single_problem(local_problem_id):
    problem_dir_path = os.path.join(DATA_DIR, local_problem_id)
    test_cases_path = os.path.join(problem_dir_path, 'test_cases.zip')
    desc_path = os.path.join(problem_dir_path, 'desc.json')
    if not os.path.exists(test_cases_path):
        return False
    result = upload_test_cases(os.path.join(problem_dir_path, 'test_cases.zip'))
    result_json = json.loads(result)
    if result_json['err']:
        return False
    with open(desc_path, 'r', encoding='utf-8') as f_desc:
        desc_row = f_desc.read()
    desc_json = json.loads(desc_row)
    desc_json['manifest'] = result_json['data']
    desc_json['manifest']['spj'] = False
    desc_json['manifest']['spj_code'] = ''
    if desc_json['source'] is None or desc_json['source'] == '':
        desc_json['source'] = '预设来源：原WUSTACM平台'
    return post_problem_desc(desc_json)


# 1081 1090 1175
if __name__ == '__main__':
    init_cookies()
    for problem_id in range(1176, 2633):
        try:
            print(problem_id)
            res = "succeed" if import_single_problem(str(problem_id)) else "failed"
        except:
            res = 'failed'
        print(f'handle {problem_id}: {res}')
        if res != 'succeed':
            with open('result', 'a') as f:
                f.write(str(problem_id) + '\n')
