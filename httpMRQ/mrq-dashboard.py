#-*- coding: utf-8 -*-
import re
import sys
from pkg_resources import load_entry_point
import time
import random

import os
import json
from mrq.task import Task
from mrq.dashboard import app as FlaskApp
from mrq.dashboard.utils import jsonify, requires_auth

from flask import request, send_from_directory, render_template_string
from mrq.job import queue_job
from mrq.context import connections

import tasks
from tool import fixTaskParams, ApiSchemaWrapper, ApiErrorBuild, HttpUrlSchema, Regex, And, Use, Optional
import jinja_filters

app = FlaskApp.app

app.jinja_env.filters['dateformat'] = jinja_filters.dateformat
app.jinja_env.filters['jsonstringify'] = jinja_filters.jsonstringify

MRQ_JOB_API = 'http://127.0.0.1:5555/api/queuejob/{{task}}/'

MRQ_TASK_DICT = {
    'tasks.Fetch': tasks.Fetch,
}

REDIS_CONFIG = {
    'subscribe_key': 'dms_hub',
    'topic_key': 'dms_topic',
}

def render_template_file(file_name, **context):
    file_path = os.path.join(os.getcwd(), 'assets', 'tpl', file_name)
    with open(file_path, 'r') as rf:
        tpl_str = rf.read().decode('utf-8')
        return render_template_string(tpl_str, **context)

random_client_id = lambda slen=8,chars='AaBbCcDdEeFfGgHhIiJjKkLMmNnoPpQqRrSsTtUuVvWwXxYyZz23456789': 'mrq'+''.join([random.choice(chars) for _ in range(slen)])
dms_topic_ext_filter = lambda ext_dict: {topic: list(set(ext_list)) for topic, ext_list in ext_dict.items() if ext_list}

@app.route('/api/queuejob/<task>/')
@requires_auth
def api_queue_job(task):  #存在参数相互依赖的关系  无法使用 ApiSchemaWrapper
    queue = request.args.get('queue', '').strip()
    params = request.args.to_dict()
    params, err = fixTaskParams(MRQ_TASK_DICT, task, params)

    rst = ApiErrorBuild()
    rst = err if not err else {"job_id": queue_job(task, params, queue=queue if queue else None)}

    return jsonify(rst)

@app.route('/dms/')
@requires_auth
def dms_list():
    pub_key = request.args.get('pub_key', '').strip()
    sub_key = request.args.get('sub_key', '').strip()
    if pub_key and sub_key:
        dmskey = '%s:%s' % (pub_key, sub_key)
        dms_list = {dmskey:connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey), }
    else:
        dms_list = connections.redis.hgetall(REDIS_CONFIG['topic_key'])

    return render_template_file('dms_list.html', DMS_LIST=[json.loads(item) for item in dms_list.values() if item], INPUT={'pub_key':pub_key, 'sub_key':sub_key})


@app.route('/dms/subscribe/')
@requires_auth
def dms_subscribe():
    pub_key = request.args.get('pub_key', '').strip()
    sub_key = request.args.get('sub_key', '').strip()
    dmskey = '%s:%s' % (pub_key, sub_key)
    dms_json = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_info = json.loads(dms_json) if dms_json else {}

    return render_template_file('dms_subscribe.html', DMS_INFO=dms_info, INPUT={'pub_key':pub_key, 'sub_key':sub_key})

@app.route('/dms/unsubscribe/')
@requires_auth
def dms_unsubscribe():
    pub_key = request.args.get('pub_key', '').strip()
    sub_key = request.args.get('sub_key', '').strip()
    dmskey = '%s:%s' % (pub_key, sub_key)
    dms_json = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_info = json.loads(dms_json) if dms_json else {}

    return render_template_file('dms_unsubscribe.html', DMS_INFO=dms_info, INPUT={'pub_key':pub_key, 'sub_key':sub_key})

@app.route('/dms/api/info/')
@requires_auth
@ApiSchemaWrapper({
    'pub_key': And(basestring, len, lambda s: s.startswith('pub_')),
    'sub_key': And(basestring, len, lambda s: s.startswith('sub_')),
}, ignore_extra_keys=True)
def dms_api_info(pub_key, sub_key):
    dmskey = '%s:%s' % (pub_key, sub_key)
    dms_info = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_json = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_info = json.loads(dms_json) if dms_json else {}

    rst = dms_info
    return rst

@app.route('/dms/api/subscribe/')
@requires_auth
@ApiSchemaWrapper({
    'pub_key': And(basestring, len, lambda s: s.startswith('pub_')),
    'sub_key': And(basestring, len, lambda s: s.startswith('sub_')),
    'topic': And(basestring, len),
    'ext': And(basestring, len, lambda s: fixTaskParams(MRQ_TASK_DICT, s.split('@', 1)[0], {'topic':'test', 'message':'{}', 'ext':s.split('@', 1)[1]})[1] is None),
}, ignore_extra_keys=True)
def dms_api_subscribe(pub_key, sub_key, topic, ext):
    dmskey = '%s:%s' % (pub_key, sub_key)
    dms_info = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_json = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_info = json.loads(dms_json) if dms_json else {}

    rst = ApiErrorBuild()
    while 1:
        if not dms_info:
            dms_info['create_time'] = time.time()

        ext_dict = dms_info.get('ext_dict', {})
        ext_set = set(ext_dict.get(topic, set()))
        if ext in ext_set:
            rst = ApiErrorBuild('ext already exists')
            break

        ext_set.add(ext)
        ext_dict[topic] = list(ext_set)
        client_id = dms_info.get('client_id', random_client_id())
        job_api = dms_info.get('job_api', MRQ_JOB_API)
        dms_msg = {'cmd':'reload', 'pub_key':pub_key, 'sub_key':sub_key, 'ext_dict':ext_dict, 'client_id': client_id, 'job_api': job_api, 'update_time': time.time()}
        dms_info.update(dms_msg)
        connections.redis.hset(REDIS_CONFIG['topic_key'], dmskey, json.dumps(dms_info))
        connections.redis.publish(REDIS_CONFIG['subscribe_key'], json.dumps(dms_msg))
        rst = {'data': dms_msg}
        break

    return rst

@app.route('/dms/api/unsubscribe/')
@requires_auth
@ApiSchemaWrapper({
    'pub_key': And(basestring, len, lambda s: s.startswith('pub_')),
    'sub_key': And(basestring, len, lambda s: s.startswith('sub_')),
    'topic': And(basestring, len),
    'ext': And(basestring, len),
}, ignore_extra_keys=True)
def dms_api_unsubscribe(pub_key, sub_key, topic, ext):
    dmskey = '%s:%s' % (pub_key, sub_key)
    dms_json = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_info = json.loads(dms_json) if dms_json else {}

    rst = ApiErrorBuild()
    while 1:
        if not dms_info:
            rst = ApiErrorBuild('dms not found')
            break
        ext_dict = dms_info.get('ext_dict', {})
        if topic not in ext_dict:
            rst = ApiErrorBuild('topic not found')
            break
        ext_set = set(ext_dict.get(topic, set()))
        if ext=='*':
            ext_set = set()
        elif ext not in ext_set:
            rst = ApiErrorBuild('ext not found')
            break
        else:
            ext_set.remove(ext)
        ext_dict[topic] = list(ext_set)
        ext_dict = dms_topic_ext_filter(ext_dict)
        client_id = dms_info.get('client_id', random_client_id())
        job_api = dms_info.get('job_api', MRQ_JOB_API)
        dms_msg = {'cmd':'reload', 'pub_key':pub_key, 'sub_key':sub_key, 'ext_dict':ext_dict, 'client_id': client_id, 'job_api': job_api, 'update_time': time.time()}
        dms_info.update(dms_msg)
        connections.redis.hset(REDIS_CONFIG['topic_key'], dmskey, json.dumps(dms_info))
        connections.redis.publish(REDIS_CONFIG['subscribe_key'], json.dumps(dms_msg))
        rst = {'data': dms_msg}
        break

    return rst

@app.route('/dms/api/remove/')
@requires_auth
@ApiSchemaWrapper({
    'pub_key': And(basestring, len, lambda s: s.startswith('pub_')),
    'sub_key': And(basestring, len, lambda s: s.startswith('sub_')),
}, ignore_extra_keys=True)
def dms_api_remove(pub_key, sub_key):
    dmskey = '%s:%s' % (pub_key, sub_key)
    dms_json = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_info = json.loads(dms_json) if dms_json else {}

    rst = ApiErrorBuild()
    while 1:
        if not dms_info:
            rst = ApiErrorBuild('dms not found')
            break

        dms_msg = {'cmd':'remove', 'pub_key':pub_key, 'sub_key':sub_key}
        connections.redis.publish(REDIS_CONFIG['subscribe_key'], json.dumps(dms_msg))
        connections.redis.hdel(REDIS_CONFIG['topic_key'], dmskey)
        rst = {'data': dms_msg}
        break

    return rst

@app.route('/dms/api/reload/')
@requires_auth
@ApiSchemaWrapper({
    'pub_key': And(basestring, len, lambda s: s.startswith('pub_')),
    'sub_key': And(basestring, len, lambda s: s.startswith('sub_')),
}, ignore_extra_keys=True)
def dms_api_reload(pub_key, sub_key):
    dmskey = '%s:%s' % (pub_key, sub_key)
    dms_json = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    dms_info = json.loads(dms_json) if dms_json else {}

    rst = ApiErrorBuild()
    while 1:
        if not dms_info:
            rst = ApiErrorBuild('dms not found')
            break
        ext_dict = dms_topic_ext_filter(dms_info.get('ext_dict', {}))
        client_id = dms_info.get('client_id', random_client_id())
        job_api = dms_info.get('job_api', MRQ_JOB_API)
        dms_msg = {'cmd':'reload', 'pub_key':pub_key, 'sub_key':sub_key, 'ext_dict':ext_dict, 'client_id': client_id, 'job_api': job_api, 'update_time': time.time()}
        dms_info.update(dms_msg)
        connections.redis.hset(REDIS_CONFIG['topic_key'], dmskey, json.dumps(dms_info))
        connections.redis.publish(REDIS_CONFIG['subscribe_key'], json.dumps(dms_msg))
        rst = {'data': dms_msg}
        break
    return rst

@app.route('/assets/<path:path>')
def assets_file(path):
    return send_from_directory('assets', path)



if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('mrq', 'console_scripts', 'mrq-dashboard')()
    )
