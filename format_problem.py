import os
import re


def check_in(x):
    return re.match(r'[\s\S]+\.in', x) is not None


def check_out(x):
    return re.match(r'[\s\S]+\.out', x) is not None


def handle_problem(problem_id, dst, src):
    src_problem_dir = os.path.join(src, problem_id)
    dst_problem_dir = os.path.join(dst, problem_id)
    os.makedirs(dst_problem_dir, exist_ok=True)
    file_list = [item for item in os.listdir(src_problem_dir)
                 if os.path.isfile(os.path.join(src_problem_dir, item))]
    in_list = list(filter(check_in, file_list))
    out_list = list(filter(check_out, file_list))
    in_list = sorted(in_list)
    out_list = sorted(out_list)
    if len(in_list) != len(out_list):
        return None
    res_list = []
    for item in range(len(in_list)):
        if in_list[item].split('.')[0] == out_list[item].split('.')[0]:
            try:
                with open(os.path.join(dst_problem_dir, f'{item + 1}.in'), 'w', encoding='utf-8') as f_in_dst:
                    with open(os.path.join(src_problem_dir, in_list[item]), 'r', encoding='utf-8') as f_in_src:
                        f_in_dst.write(f_in_src.read())
                res_list.append(f'{item + 1}.in')
            except Exception as e:
                print('in file error:', in_list[item])
                raise e
            try:
                with open(os.path.join(dst_problem_dir, f'{item + 1}.out'), 'w', encoding='utf-8') as f_out_dst:
                    with open(os.path.join(src_problem_dir, out_list[item]), 'r', encoding='utf-8') as f_out_src:
                        f_out_dst.write(f_out_src.read())
                res_list.append(f'{item + 1}.out')
            except Exception as e:
                print('out file error:', out_list[item])
                raise e
    return res_list
