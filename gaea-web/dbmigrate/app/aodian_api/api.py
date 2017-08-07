# coding: utf-8

import requests
import time
from urllib import quote

def _res_rst(res, api, _params, start_time, is_log):
    use_time = int((time.time() - start_time) * 1000)
    if res.ok:
        rst = res.json()
        if is_log:
            print '%s(%dms) [INFO] params:%r, rst:%r' % (api, use_time, _params, rst)
        return rst
    else:
        if is_log:
            print '%s(%dms) [ERROR] url:%s, params:%r, res:$r' % (api, use_time, query_url, _params, res)
        return {}

class AoDianWis(object):
    pass

class LCPSApi(object):
    pass

class AodianApi(object):
    api_url = 'http://openapi.aodianyun.com/v2/'

    def __init__(self, access_id, access_key):
        self.access_id, self.access_key = (access_id, access_key)

    def openApi(self, api, _params, is_log = False):
        start_time = time.time()
        params = dict(_params)
        params.setdefault('access_id', self.access_id)
        params.setdefault('access_key', self.access_key)
        add_header = {
            "Content-type": "application/json; charset=UTF-8",
            'Accept': 'application/json',
        }
        query_url = AodianApi.api_url + api;
        res = requests.post(query_url, json=params, headers=add_header)
        return _res_rst(res, api, _params, start_time, is_log)


class AoDianDms(object):
    api_url = 'http://api.dms.aodianyun.com/v1/'
    api_url_v2 = 'http://api.dms.aodianyun.com/v2/'

    def __init__(self, dms_s_key):
        self.dms_s_key = dms_s_key

    def usersTopic(self, topic, skip=0, num=20, is_log = False):
        topic = quote(topic)
        if not topic:
            return {}
        api = "topics/%s/users?skip=%d&num=%d" % (topic, skip, num)
        return self.dmsApi(api, is_log=is_log)

    def messagesClientId(self, client_id, msg, is_log = False):
        api = "messages/p2p/%s" % (client_id, )
        params = {'body': msg}
        return self.dmsApi(api, json.dumps(params), 'POST', is_log=is_log)

    def messagesTopic(self, topic, msg, is_log = False):
        msg = json.dumps(msg)
        topic = quote(topic)
        api = "messages/%s" % (topic)
        params = {'body': msg}
        return self.dmsApi(api, json.dumps(params), 'POST', is_log=is_log)

    def historysDel(self, _id, is_log = False):
        topic = quote(topic)
        api = "historys/%s/%s" % (topic, _id)
        return self.dmsApi(api, {}, 'DELETE', is_log=is_log)

    def historys_v2(self, topic, skip, num, startTime='', endTime='', is_log = False):
        topic = quote(topic)
        api = 'historys?skip=%d&num=%d&topic=%s&startTime=%s&endTime=%s' % (skip, num, topic, startTime, endTime)
        return self.dmsApi_v2(api, is_log=is_log)

    def historys(self, topic, start, num_message, is_log = False):
        topic = quote(topic)
        api = "historys/%s/%d/%d" % (topic, start, num_message)
        return self.dmsApi_v2(api, is_log=is_log)

    def dmsApi(self, api, _params={}, method='get', is_log = False):
        start_time = time.time()
        params = _params if _params else ''
        add_header = {
            "Content-type": "application/json; charset=UTF-8",
            'Accept': 'application/json',
            'Authorization': 'dms ' + self.dms_s_key
        }
        query_url = self.api_url + api
        res = requests.request(method.lower(), query_url, data=params, headers=add_header)
        return _res_rst(res, api, _params, start_time, is_log)

    def dmsApi_v2(self, api, _params={}, method='get', is_log = False):
        start_time = time.time()
        params = _params if _params else ''
        add_header = {
            "Content-type": "application/json; charset=UTF-8",
            'Accept': 'application/json',
            'Authorization': 'dms ' + self.dms_s_key
        }
        query_url = self.api_url_v2 + api
        res = requests.request(method.lower(), query_url, data=params, headers=add_header)
        return _res_rst(res, api, _params, start_time, is_log)

class Config(object):
    def __init__(self, dict_in):
        dict_in = {k: Config(v) if isinstance(v, dict) else v for k, v in dict_in.items()}
        self.__dict__.update(dict_in)

    def __str__(self):
        return str({k: str(v) for k, v in self.__dict__.items()})


if __name__ == '__main__':
    import os, json
    with open(os.path.join(os.getcwd(), 'test_config.ignore.json')) as rf:
        conf = Config(json.load(rf))

    AodianApi(conf.access_id, conf.access_key).openApi('LSS.GetAppLiveStatus', {
        'appid': conf.lss_app,
        'stream': conf.stream,
    }, is_log=True)

    AodianApi(conf.access_id, conf.access_key).openApi('LSS.GetApp', {
        'num': 2,
        'page': 1,
    }, is_log=True)

    AoDianDms(conf.dms_s_key).historys_v2(conf.topic, 0, 20, is_log=True)
    msg = u'{"msg_id":644,"user":{"user_id":"tmp23169","nick":"\\u6e38\\u5ba2-23169","avatar":"http:\\/\\/58jinrongyun.com\\/dist\\/dyy\\/view\\/jiaoyu\\/mobile\\/images\\/male.png","user_type":"guest"},"msgContent":{"msg_status":"review_add","target_msg_id":null,"target_user_id":null,"content_text":"FFFFF","operator_id":null},"msg_type":"chat_and_review","room_id":177,"timestamp":1496822172,"cmd":"chat_and_review"}'
    AoDianDms(conf.dms_s_key).messagesTopic(conf.topic, json.loads(msg), is_log=True)





