# -*- coding: utf-8 -*-
import re
import os
import csv

def run(url_file, save_seq = 10000):
    '''
       log_format main  '$remote_addr $host [$time_local] "$request" '
                     '$status $request_length $body_bytes_sent "$http_referer" "$http_user_agent" '
                     '"$server_addr" "$upstream_addr" "$http_x_forwarded_for" "$upstream_cache_status" $upstream_response_time $request_time';
                     
    '''
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
                print '.',

    return calculateAverage(ret_data)

def calculateAverage(ret_data):
    for key, val in ret_data.iteritems():
        val['average_request_time'] = val['total_request_time'] / val['num']
        val['average_request_length'] = val['total_request_length'] / val['num']
        val['average_body_bytes_sent'] = val['total_body_bytes_sent'] / val['num']

    return ret_data

def writeCsv(csv_file, ret_data):
    with open(csv_file, 'wb') as csvfile:
        fieldnames = ['url', ] + ret_data[ ret_data.keys()[0] ].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for url, item in ret_data.iteritems():
            item['url'] = url
            writer.writerow(item)

def main():
    print '\n---------------Start-------------------\n'

    _url_file = 'access.log'
    _csv_file = _url_file + '.csv'
    
    csv_file = os.path.join(os.getcwd(), _csv_file)
    url_file = os.path.join(os.getcwd(), _url_file)
    
    ret_data = run(url_file)
    writeCsv(csv_file, ret_data)
    
    print '\n---------------End--------------------\n'

if __name__ == '__main__':
    main()