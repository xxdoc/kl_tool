# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#https://pypi.tuna.tsinghua.edu.cn/simple
import os
import json

def main():
    config = load_json( cwd('gitrepo_config.ignore') )
    cfg = fix_config(config)

    str_map = build_push_map(cfg)

    bat_lines = ['@ECHO ON']
    idx, seq = 0, 6
    bash = 'D:\\Git\\git-bash.exe'
    for repo, str_list in str_map.items():
        idx += 1
        sh = cwd('gitrepo', '%s.gitbash' % (repo, ))
        is_wait = '/wait' if idx % seq == 0 or idx == len(str_map)  else ''
        dump_file(sh, [line + '\n' for line in str_list])
        bat_lines.append('start %s %s %s' % (is_wait, bash, sh))

    bat_lines.append('PAUSE')
    dump_file(cwd('git-push.bat'), [line + '\n' for line in bat_lines])

def fix_config(config):
    cfg = {}
    for key, val in config.items():
        if not key:
            continue
        path = val.pop('WorkPath', '')
        remote = dict(val)
        if not path or not os.path.isdir(path) or not remote:
            continue
        cfg.setdefault(key, {'path': _fix_path(path), 'remote': remote})
    return cfg

def _fix_path(path):
    tmp_list = path.split(':\\', 1)
    return '/{drive}/{dirpath}'.format(drive=tmp_list[0].lower(), dirpath=tmp_list[1].replace('\\', '/'))

def build_push_map(cfg):
    repo_map = {}
    for name, item in cfg.items():
        str_list =[]
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
                'git push {repo} --all -f'.format(repo=k),
                'git push {repo} --tags -f'.format(repo=k),
                'git remote remove {repo}'.format(repo=k),
                'echo "done {repo}"'.format(repo=k),
                'echo " "',
            ])

        str_list.append('exit')
        ret_list = []
        for line in str_list:
            if not line.startswith('echo'):
                ret_list.append('echo "> {cmd}"'.format(cmd=line))
            ret_list.append(line)

        repo_map[name] = ret_list

    return repo_map

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
