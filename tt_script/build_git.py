# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#https://pypi.tuna.tsinghua.edu.cn/simple
import os
import json

def main():
    config = load_json( cwd('gitrepo_config.ignore') )
    cfg = fix_config(config)
    str_list = build_push(cfg)
    dump_file(cwd('gitrepo.gitbash'), [line + '\n' for line in str_list])

def fix_config(config):
    cfg = {}
    for key, val in config.items():
        path = val.pop('WorkPath', '')
        remote = dict(val)
        if not path or not os.path.isdir(path) or not remote:
            continue
        cfg.setdefault(key, {'path': _fix_path(path), 'remote': remote})
    return cfg

def _fix_path(path):
    tmp_list = path.split(':\\', 1)
    return '/{drive}/{dirpath}'.format(drive=tmp_list[0].lower(), dirpath=tmp_list[1].replace('\\', '/'))

def build_push(cfg):
    str_list =[]
    for name, item in cfg.items():
        remote = item['remote']
        str_list.extend([
            'cd {path}'.format(path=item['path']),
            '''git branch -r | grep -v '\->' | while read remote; do git branch --track "${remote#origin/}" "$remote"; done''',
            'git fetch --all',
            'git pull --all',
        ])
        for k,v in remote.items():
            str_list.extend([
                'git remote add {repo} {url}'.format(repo=k, url=v),
                'git push {repo} --all'.format(repo=k),
                'git push {repo} --tags'.format(repo=k),
                'git remote remove {repo}'.format(repo=k),
            ])
    str_list.append('exit')
    ret_list = []
    for line in str_list:
        ret_list.append('echo "> {cmd}"'.format(cmd=line))
        ret_list.append(line)
    return ret_list

def cwd(*f):
    return os.path.join(os.getcwd(), *f)

def dump_file(file_name, str_list):
    if not os.path.isdir(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    with open(file_name, 'w') as wf:
        wf.writelines(str_list)
        print "write file:%s" % (file_name, )

def load_file(file_name):
    if not os.path.isfile(file_name):
        return ''
    with open(file_name, 'r') as rf:
        return rf.read()

def load_json(file_name):
    with open(file_name, 'r') as rf:
        return json.load(rf)

if __name__ == '__main__':
    main()