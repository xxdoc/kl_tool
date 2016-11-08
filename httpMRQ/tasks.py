#-*- coding: utf-8 -*-
from mrq.task import Task
from mrq.context import log

from tool import getUrl, getProxy, TaskSchemaWrapper, HttpUrlSchema, Regex, And, Use, Optional

class Fetch(Task):

    @TaskSchemaWrapper({'topic': And(str, len), 'message': And(str, len), 'ext': HttpUrlSchema}, ignore_extra_keys=True)
    def run(self, params):
        url = params.get('url', '').strip()
        topic = params.get('topic', '').strip()
        message = params.get('message', '').strip()
        ext_url = 'topic=' + topic + '&message' + message
        if '?' not in url:
            url = url + '?' + ext_url
        else:
            url = url + ext_url if url.endswith('&') else url + '&' + ext_url
        log.info('HTTP GET %s' % (url, ))
        return getUrl(url, use_gzip=False, proxy_info=None)
