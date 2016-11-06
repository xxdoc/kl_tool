#-*- coding: utf-8 -*-
from mrq.task import Task
from schema import Regex, And, Use, Optional
from tool import getUrl, getProxy, SchemaWrapper
import re


class Fetch(Task):

    @SchemaWrapper({'url': And(basestring, len, Regex('^(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?$'))}, ignore_extra_keys=True)
    def run(self, params):
        url = params.get('url', '')
        return getUrl(url, proxy_info=None)
