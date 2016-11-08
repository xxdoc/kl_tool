#-*- coding: utf-8 -*-
import re
import sys
from pkg_resources import load_entry_point

import os
import json
from mrq.task import Task
from mrq.dashboard import app as FlaskApp
from flask import request, send_from_directory, render_template_string
from mrq.job import queue_job
from mrq.context import connections

import tasks
from tool import fixParams

jsonify = FlaskApp.jsonify
requires_auth = FlaskApp.requires_auth
app = FlaskApp.app

ALLOW_TASK_DICT = {
    'tasks.Fetch': tasks.Fetch,
}

REDIS_CONFIG = {
    'subscribe_key': 'dms_hub',
    'topic_key': 'dms_topic',
}

def render_template_file(file_name, **context):
    with open(file_name, 'r') as rf:
        tpl_str = rf.read().decode('utf-8')
        return render_template_string(tpl_str, **context)

@app.route('/api/queuejob/<task>/')
@requires_auth
def api_queue_job(task):
    queue = request.args.get('queue', '').strip()
    params, err = fixParams(ALLOW_TASK_DICT, task, request.args.to_dict())
    return jsonify(err) if not err is None else jsonify({
        "job_id": queue_job(task, params, queue=queue if queue else None)
    })

@app.route('/dms/')
@requires_auth
def dms_list():
    pub_key = request.args.get('pub_key', '').strip()
    sub_key = request.args.get('sub_key', '').strip()
    page = int(request.args.get('page', '1').strip())
    limit = int(request.args.get('limit', '20').strip())
    dms_list = connections.redis.hgetall(REDIS_CONFIG['topic_key'])
    tpl_file = os.path.join(os.getcwd(), 'assets', 'tpl','dms_list.html')
    return render_template_file(tpl_file, DMS_LIST=dms_list)

@app.route('/dms/edit/<dmskey>/')
@requires_auth
def dms_edit(dmskey):
    dms_info = connections.redis.hget(REDIS_CONFIG['topic_key'], dmskey)
    tpl_file = os.path.join(os.getcwd(), 'assets', 'tpl','dms_edit.html')
    return render_template_file(tpl_file, DMS_INFO=dms_info)

@app.route('/dms/new/')
@requires_auth
def dms_new():
    tpl_file = os.path.join(os.getcwd(), 'assets', 'tpl','dms_new.html')
    return render_template_file(tpl_file)

@app.route('/assets/<path:path>')
def assets_file(path):
    return send_from_directory('assets', path)

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('mrq', 'console_scripts', 'mrq-dashboard')()
    )
