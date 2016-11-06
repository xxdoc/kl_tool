#-*- coding: utf-8 -*-
__requires__ = 'mrq==0.1.12'
import re
import sys
from pkg_resources import load_entry_point

import os
import json
from mrq.task import Task
from mrq.dashboard import app as FlaskApp
from flask import request
from mrq.job import queue_job

import tasks
from tool import fixParams

jsonify = FlaskApp.jsonify
requires_auth = FlaskApp.requires_auth
app = FlaskApp.app

ALLOW_TASK_DICT = {
    'tasks.Fetch': tasks.Fetch,
}


@app.route('/api/queuejob/<task>/')
@requires_auth
def api_queue_job(task):
    queue = request.args.get('queue', '').strip()
    params, err = fixParams(ALLOW_TASK_DICT, task, request.args.to_dict())
    return jsonify(err) if not err is None else jsonify({
        "job_id": queue_job(task, params, queue=queue if queue else None)
    })


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('mrq==0.1.12', 'console_scripts', 'mrq-dashboard')()
    )
