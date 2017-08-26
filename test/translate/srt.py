#coding=utf8
import md5
import urllib
import random
import requests
import re
import cPickle
import os

from config_ignore import BAIDU_TRANSLATE_APP_ID, BAIDU_TRANSLATE_SECRET_KEY
#从配置文件 获取 百度翻译API appid 和 secretKey 你可以直接在这里配置

def md5str(string):
    m1 = md5.new()
    m1.update(string)
    return m1.hexdigest()

def baidu_translate(en_list, fromLang='en', toLang='zh', appid=BAIDU_TRANSLATE_APP_ID, secretKey=BAIDU_TRANSLATE_SECRET_KEY):
    api = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    q = '\n' . join(en_list)
    salt = str(random.randint(32768, 65536))
    sign_str = appid + q + salt + secretKey

    payload = {
        'appid': appid,
        'q' : q,
        'from' : fromLang,
        'to': toLang,
        'salt': salt,
        'sign': md5str(sign_str),
    }
    res = requests.post(api, params=payload)
    ret_dict = {en:'' for en in en_list}
    try:
        ret_list = res.json().get('trans_result', [])
    except Exception as ex:
        print 'error'

    ret_dict.update({item.get('src', ''):item.get('dst', '') for item in ret_list})
    return ret_dict

def save_srt(file_name, file_lines):
    with open(file_name, 'w') as wf:
        wf.writelines([line+"\n" for line in file_lines])

def read_srt(file_name):
    with open(file_name, 'r') as rf:
        file_lines = rf.readlines()

    re_tmp = re.compile('^[\d]{2}:[\d]{2}:[\d]{2},[\d]{3}')
    need_translate = lambda s: False if not s or s.isalnum() or re_tmp.match(s) else True

    en_dict = {}
    for idx, line in enumerate(file_lines):
        tmp = line.strip()
        if need_translate(tmp):
            en_dict.setdefault(tmp, [])
            en_dict[tmp].append(idx)

    return file_lines, en_dict

def list_translate(srt_file, all_list, use_tmp=True):
    dump_file = srt_file+'.translate'
    if use_tmp and os.path.isfile(dump_file):
        with open(dump_file, 'r') as rf:
            return cPickle.load(rf)

    task = []
    ret_dict = {}
    while all_list:
        task.append(all_list.pop())
        if len(task)>=100:
            ret_dict.update(baidu_translate(task))
            print '%s list_translate task:%s last:%s' % (srt_file, len(task), len(all_list))
            task = []
    if task:
        ret_dict.update(baidu_translate(task))
        print '%s list_translate task:%s last:%s' % (srt_file, len(task), len(all_list))

    with open(dump_file, 'w') as wf:
        cPickle.dump(ret_dict, wf)
    return ret_dict

def srt_translate(srt_file):
    file_lines, en_dict = read_srt(srt_file)
    translate_dict = list_translate(srt_file, en_dict.keys())

    for en, zh in translate_dict.items():
        idx_list = en_dict.get(en, [])
        for idx in idx_list:
            file_lines[idx] = en + zh.encode('utf-8')

    out_file = srt_file.replace('.en.srt', '.enzh.srt')
    save_srt(out_file, file_lines)
    return out_file

def main():
    file_list = [item for item in os.listdir(os.getcwd()) if item.endswith('.en.srt') and os.path.isfile(item)]
    print [srt_translate(srt_file) for srt_file in file_list]

if __name__ == '__main__':
    main()