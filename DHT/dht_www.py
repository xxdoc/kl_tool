# -*- coding: utf-8 -*-
import json
import web
import dht_api as API

urls = (
    '/api/([A-Za-z0-9=_]+)', 'Apijson',
    '/(.*)', 'Home',
)

class Home:
    def GET(self, args=None):
        return "Hello World!"

class Apijson:
    def GET(self, func):
        api = web.input(func="apihelp", args='', indent='', callback='')
        func = getattr(API, func, API.apihelp)

        if not getattr(func, 'is_api', False):
            raise NOT_FOUND("404 Run Error:%r." % ('bad func name',))

        try:
            args = func.args_parser(api.args, api)
            result = func(args)

            indent = api.indent
            indent=int(indent) if indent and indent.isdigit() else None
            json_str = json.dumps(result, indent=indent)
            return json_str if not api.callback else '%s(%s);' % (api.callback, json_str)
        except Exception as ex:
            raise NOT_FOUND("404 Run Error:%r." % (ex,))



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()