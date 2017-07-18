# -*- coding: utf-8 -*-

import re
import os
import cPickle

def dump_obj(file_name, obj):
    with open(file_name, 'wb') as wf:
        cPickle.dump(obj, wf)

def load_obj(file_name):
    if not os.path.isfile(file_name):
        return None
    with open(file_name, 'rb') as rf:
        return cPickle.load(rf)


def run(url_file, obj_file, save_seq = 10000):
    '''
    log_format main  '$remote_addr $host [$time_local] "$request" '
                     '$status $request_length $body_bytes_sent "$http_referer" "$http_user_agent" '
                     '"$server_addr" "$upstream_addr" "$http_x_forwarded_for" "$upstream_cache_status" $upstream_response_time $request_time';'''

    reg_str = r'^([\S]+)\s([\S]+)\s(\[(.*)\])\s\"([A-Z]+)\s([\S]+)\s([^"]+)\"\s([\d]+)\s([\d]+)\s([\d]+)\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s\"([^"]+)\"\s([0-9.]+)\s([0-9.]+)$'
    reg = re.compile(reg_str)
    ret_data = {}

    with open(url_file, 'r') as rf:
        for idx, line in enumerate(rf):
            tmp = reg.match(line)
            if not tmp:
                continue
            tmp_list = tmp.groups()
            remote_addr, host, time_local, request_method, request_uri, \
                request_protocol, status, request_length, body_bytes_sent, \
                    http_referer, http_user_agent, server_addr, upstream_addr, \
                        http_x_forwarded_for, upstream_cache_status, upstream_response_time, \
                            request_time = tmp_list[1:]

            if request_uri == '-':
                continue

            req_list = request_uri.split('?')
            request_path = req_list[0]
            request_query = req_list[1] if len(req_list) > 1 else ''
            if request_path in ret_data:
                ret_data[ request_path ]['num'] += 1
                ret_data[ request_path ]['total_request_time'] += float(request_time)
                ret_data[ request_path ]['total_request_length'] += float(request_length)
                ret_data[ request_path ]['total_body_bytes_sent'] += float(body_bytes_sent)
                if status in ret_data[ request_path ]['status_map']:
                    ret_data[ request_path ]['status_map'][ status ] += 1
                else:
                    ret_data[ request_path ]['status_map'][ status ] = 1
            else:
                ret_data.setdefault(request_path, {
                    'num': 1, 'status_map': {status: 1},
                    'total_request_time': float(request_time),
                    'total_request_length': float(request_length),
                    'total_body_bytes_sent': float(body_bytes_sent),
                })


            if idx % save_seq == 1:
                ret_data = calculateAverage(ret_data)
                print '.',
                dump_obj(obj_file, ret_data)

    return calculateAverage(ret_data)



def calculateAverage(ret_data):
    for key, val in ret_data.iteritems():
        val['average_request_time'] = val['total_request_time'] / val['num']
        val['average_request_length'] = val['total_request_length'] / val['num']
        val['average_body_bytes_sent'] = val['total_body_bytes_sent'] / val['num']

    return ret_data

def writeCsv(csv_file, ret_data):
    import csv
    with open(csv_file, 'wb') as csvfile:
        fieldnames = ['url', ] + ret_data['/'].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for url, item in ret_data.iteritems():
            item['url'] = url
            writer.writerow(item)

def main():
    csv_file = 'access_20170627.csv'
    url_file = 'access_20170627.access_log'
    obj_file = '_tmp_access_log.obj'
    csv_file = os.path.join(os.getcwd(), csv_file)
    url_file = os.path.join(os.getcwd(), url_file)
    obj_file = os.path.join(os.getcwd(), obj_file)


    print '\n---------------Start-------------------\n'
    ret_data = run(url_file, obj_file)
    print '\n---------------End--------------------\n'
    dump_obj(obj_file, ret_data)

    ret_data = load_obj(obj_file)
    writeCsv(csv_file, ret_data)
    return

if __name__ == '__main__':
    main()