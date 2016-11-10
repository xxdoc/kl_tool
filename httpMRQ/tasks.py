#-*- coding: utf-8 -*-
from mrq.task import Task
from mrq.context import log
import requests
from tool import TaskSchemaWrapper, HttpUrlSchema, Regex, And, Use, Optional

class Fetch(Task):

    @TaskSchemaWrapper({'topic': And(basestring, len), 'message': And(basestring, len), 'ext': HttpUrlSchema}, ignore_extra_keys=True)
    def run(self, params):
        url = params.get('ext', '').strip()
        topic = params.get('topic', '').strip()
        message = params.get('message', '').strip()
        ext_url = 'topic=' + topic + '&message' + message
        if '?' not in url:
            url = url + '?' + ext_url
        else:
            url = url + ext_url if url.endswith('&') else url + '&' + ext_url
        log.info('HTTP GET %s' % (url, ))
        res = requests.get(url)
        if res.ok:
            return res.content
        else:
            retry_current_job()
