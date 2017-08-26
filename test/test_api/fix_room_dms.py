# -*- coding: utf-8 -*-
import requests
import os
import cPickle
import json

def dump_obj(file_name, obj):
    with open(file_name, 'wb') as wf:
        cPickle.dump(obj, wf)

def load_obj(file_name):
    with open(file_name, 'rb') as rf:
        return cPickle.load(rf)

def get_url_set(url_file, tmp_file):
    if os.path.isfile(tmp_file):
        return load_obj(tmp_file)
    elif os.path.isfile(url_file):
        with open(url_file, 'r') as rf:
            args_list = build_args(rf.readlines())
            tmp_set = list( [build_params(room_id, timestamp, num) for (room_id, timestamp, num) in args_list] )
            dump_obj(tmp_file, tmp_set)
            return tmp_set

def build_args(lines):
    def _get_agrs(line):
        args = json.loads(line)
        room_id, timestamp, num = args.get('topic', '').replace('chat_', ''), args.get('uptime', ''), args.get('total', '0')
        room_id, timestamp, num = int(room_id), int(timestamp), int(num)
        return (room_id, timestamp, num) if num > 0 else None

    tmp_list = [_get_agrs(line) for line in lines if _get_agrs(line)]
    room_map = {}
    for tmp in tmp_list:
        room_map.setdefault(tmp[0], [])
        room_map[tmp[0]].append( (tmp[1], tmp[2]) )

    ret_list = []
    for room_id, room_data in room_map.items():
        room_data = fix_timestamp_num(room_data)
        ret_list.extend([(room_id, timestamp, num) for (timestamp, num) in room_data])

    return ret_list

def fix_timestamp_num(room_data, per_sec=600):
    time_count_dict = {}
    for (timestamp, num) in room_data:
        time_count = int(timestamp / per_sec)
        time_count_dict.setdefault(time_count, {'num':0, 'total':0, 'tnum':0})
        time_count_dict[ time_count ]['total'] += num
        time_count_dict[ time_count ]['tnum'] += 1
    for k, v in time_count_dict.iteritems():
        v['num'] = int(v['total'] / v['tnum'])

    t_keys = time_count_dict.keys()
    t_keys.sort()
    pair_list = []
    next_item = t_keys.pop(0)
    while t_keys:
        t = t_keys.pop(0)
        pair = (next_item, t)
        next_item = t
        pair_list.append(pair)

    ret_list = []
    for (a_idx, b_idx) in pair_list:
        a_num, b_num = time_count_dict[a_idx]['num'], time_count_dict[b_idx]['num']
        ret_list.append((a_idx * per_sec, a_num))
        for idx in range(a_idx + 1, b_idx):
            num = int((a_num + b_num) / 2)
            ret_list.append((idx * per_sec, num))
    else:
        if pair_list:
            num = time_count_dict[b_idx]['num']
            ret_list.append((b_idx * per_sec, num))
            ret_list.append((b_idx * per_sec + per_sec, num))

    return ret_list

def build_params(room_id, timestamp, num):
    if not all([room_id, timestamp]):
        raise ValueError('empty args')

    base_url = 'http://58jinrongyun.com/api/DmsNodeHelper/fixRoomDmsRecord?'
    args_url = 'room_id=%s&timestamp=%s&num=%s' % (room_id, timestamp, num)
    return base_url + args_url

def main():
    tmp_file = '_tmp_room_dms.obj'
    url_file = 'api_args.txt'


    url_set = set(get_url_set(url_file, tmp_file))

    while url_set:
        url = url_set.pop()
        print url
        res = requests.get(url)
        if res.ok:
            print res.content
            dump_obj(tmp_file, url_set)


if __name__ == '__main__':
    main()
