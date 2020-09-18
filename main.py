import json
import os
import yaml
import format_problem
import traceback
import zipfile
from multiprocessing import Pool

src_dir = 'dist'
dst_dir = 'destination'


class Problem:
    def __init__(self, data: dict):
        if not data:
            raise Exception('Problem Information Required.')
        self.title = data.get('title', '')
        self.time_limit = data.get('time_limit', 1) * 1000
        self.memory_limit = data.get('memory_limit', 128)
        self.source = data.get('source', '')
        self.author = data.get('author', '')
        self.public = 0
        self.content = {
            'legacy': {
                'description': data.get('description', ''),
                'input': data.get('input', ''),
                'output': data.get('output', ''),
                'sample_input': data.get('sample_input', ''),
                'sample_output': data.get('sample_output', ''),
                'hint': data.get('hint', ''),
            }
        }
        self.manifest = {
            'spj': data.get('spj', '0') == '1',
            'spj_code': ''
        }


def load_file():
    with open('problem.json', 'r', encoding='utf-8') as f:
        fin = f.read()
    return json.loads(fin.replace('\\r\\n', '\\n'))


def handle_problem(item):
    problem = Problem(item)
    if problem.manifest['spj']:
        return
    problem_id = str(item['problem_id'])
    problem_path = os.path.join(dst_dir, problem_id)
    try:
        test_cases_list = format_problem.handle_problem(problem_id=problem_id, dst=dst_dir, src=src_dir)
        if not test_cases_list or len(test_cases_list) == 0:
            return
        test_cases_zip = zipfile.ZipFile(os.path.join(problem_path, 'test_cases.zip'), 'w')
        for filename in test_cases_list:
            test_cases_zip.write(os.path.join(problem_path, filename), filename)
        test_cases_zip.close()
    except Exception:
        print('Error occurred', problem_id)

    with open(os.path.join(problem_path, 'desc.yaml'), 'w', encoding='utf-8') as fin1:
        yaml.dump(problem,
                  fin1,
                  indent=None,
                  allow_unicode=True)
    with open(os.path.join(problem_path, 'desc.json'), 'w', encoding='utf-8') as fin2:
        fin2.write(json.dumps(problem.__dict__, ensure_ascii=False, indent=4))
    print('success ', problem_id)


def main():
    my_pool = Pool(4)
    _problems = load_file()
    for item in _problems:
        my_pool.apply_async(handle_problem, (item,))
    my_pool.close()
    my_pool.join()


if __name__ == '__main__':
    main()
