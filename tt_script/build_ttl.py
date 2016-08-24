# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
import os
import json

def main():
    config = load_json( cwd('server_config.ignore') )
    cfg = fix_config(config);
    for key, item in cfg.items():
        str_list = connect_ttl(key, item)
        dump_file(cwd(key+'.ttl'), str_list)
        str_list = clear_log_ttl(key, item)
        dump_file(cwd('clear_log', key+'_clear.ttl'), str_list)

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

def fix_config(cfg):
    base_ini = load_file(cwd('_tt_config_ini', 'TERATERM_TPL.INI'))
    rst = {}
    for key, item in cfg.items():
        item['Prompt'] = '#' if item['User']=='root' else '$'
        dump_file(cwd('_tt_config_ini', 'tmp', key+'.INI'), base_ini.replace('{{TPL_TITLE}}', key, 1))
        item['Ini'] = cwd('_tt_config_ini', 'tmp', key+'.INI')
        item['FirstCmd'] = 'ps -ef | grep node' if key.find('node')>=0 else 'ps -ef | grep "nginx\|httpd"'
        rst[key] = item
    return rst

def _append(str_list, str_append):
    str_list.append(str_append)
    return str_list

def base_ttl(key, item):
    return [
        "set_Title ='%s' \n" % (key, ),
        "set_Prompt = '%s' \n" % (item['Prompt'], ),
        "set_Host = '%s' \n" % (item['Host'], ),
        "set_User = '%s' \n" % (item['User'], ),
        "set_Password = '%s' \n" % (item['Password'], ),
        "set_Ini = '%s' \n" % (item['Ini'], ),
        "set_FirstCmd  = '%s' \n" % (item['FirstCmd'], ),
        "set_WorkPath = '%s' \n" % (item['WorkPath'], ),
        """
;++++++++++++++++++++++++++++++++++++++++++++
tmp_connect_cmd = ''
strconcat tmp_connect_cmd set_Host
strconcat tmp_connect_cmd ' /ssh /2 /auth=password'
strconcat tmp_connect_cmd ' /user='
strconcat tmp_connect_cmd set_User
strconcat tmp_connect_cmd ' /passwd='
strconcat tmp_connect_cmd set_Password
strconcat tmp_connect_cmd ' /f='
strconcat tmp_connect_cmd set_Ini
connect tmp_connect_cmd """,
    ]

def connect_ttl(key, item):
    return _append(base_ttl(key, item), """
;++++++++++++++++++++++++++++++++++++++++++++
tmp_cd_cmd = 'cd '
strconcat tmp_cd_cmd set_WorkPath

wait set_Prompt
sendln set_FirstCmd
wait set_Prompt
sendln tmp_cd_cmd
wait set_Prompt
sendln 'pwd'
wait set_Prompt
sendln 'git branch -a'
wait set_Prompt
sendln 'pwd'
wait set_Prompt
sendln 'git log -1'
wait set_Prompt
;++++++++++++++++++++++++++++++++++++++++++++
settitle set_Title
restoresetup set_Ini
""")

def clear_log_ttl(key, item):
    return _append(base_ttl(key, item), """
;++++++++++++++++++++++++++++++++++++++++++++
tmp_cd_cmd = 'cd '
strconcat tmp_cd_cmd set_WorkPath

wait set_Prompt
sendln tmp_cd_cmd
wait set_Prompt
sendln 'pwd'
wait set_Prompt
sendln 'rm -rf ./log/*'
wait set_Prompt
;++++++++++++++++++++++++++++++++++++++++++++
settitle set_Title
restoresetup set_Ini
disconnect
closett
""")

if __name__ == '__main__':
    main()
