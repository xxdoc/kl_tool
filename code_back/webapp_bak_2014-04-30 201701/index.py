# -*- coding: utf-8 -*-

import web

urls = (
    '/(.*)', 'index'
    )

head_str = '$def with(title)\n<!DOCTYPE html><!--STATUS OK--><html><head><meta http-equiv="content-type" \
content="text/html;charset=utf-8"><title>$title</title>'
head_st = web.template.Template(head_str)

wowdb = web.database(host='127.0.0.1',dbn='mysql', user='root', pw='root', db='wow_ah_db', charset='utf8')

class index:
    def GET(self, name):
        if not name:
            return str(head_st('Null Name')) + "Null Name."
        fwq = str(name)
        fwq = fwq.lower()
        fwqdb = wowdb.query('select * from aa_fwq_info where name=$fwq',vars={'fwq':fwq})
        if len(fwqdb)==1:
            n=fwqdb[0]
            return "".join([str(head_st(n['name'])),n['zname']," \t",n['name']," \t",n['slug']," \t",str(n['time'])\
                            ," \t",str(n['last'])," \t",str(n['fsize'])," \t",n['dir']])
        else:
            return str(head_st('Error Name')) + " Error Name!"


app = web.application(urls, globals(), autoreload=True)
application = app.wsgifunc()


