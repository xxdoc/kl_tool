#-*- coding: utf-8 -*-
import json
import tasks
from tool import fixParams

ALLOW_TASK_DICT = {
    'tasks.Fetch': tasks.Fetch,
}

jsonify = json.dumps

def test_queue_job(task, params):
    params, err = fixParams(ALLOW_TASK_DICT, task, params)
    return jsonify(err) if not err is None else jsonify({
        "job_id": {'task':task, 'params':params}
    })

def main():
    print test_queue_job('adawd', {})
    print test_queue_job('', {})
    print test_queue_job(123, {})
    print test_queue_job(None, {})

    print test_queue_job('tasks.Fetch', {})
    print test_queue_job('tasks.Fetch', {'url': 123})
    print test_queue_job('tasks.Fetch', {'url': ''})
    print test_queue_job('tasks.Fetch', {'url': 'http://g.cn'})
    print test_queue_job('tasks.Fetch', {'url': 'httP://g.cn'})
    print test_queue_job('tasks.Fetch', {'url': 'https://g.cn'})

if __name__ == '__main__':
    main()