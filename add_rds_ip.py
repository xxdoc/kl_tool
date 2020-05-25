# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#https://pypi.tuna.tsinghua.edu.cn/simple
import os
import json
import requests
import datetime

from aliyunsdkcore.client import AcsClient
from aliyunsdkrds.request.v20140815 import CreateDBInstanceRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceIPArrayListRequest
from aliyunsdkrds.request.v20140815 import ModifySecurityIpsRequest

def cwd(*f):
    return os.path.join(os.getcwd(), *f)

def dump_file(file_name, str_list):
    if not os.path.isdir(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    with open(file_name, 'w') as wf:
        wf.writelines(str_list)
        print "write file:%s" % (file_name, )

def load_file(file_name):
    if not os.path.isfile(file_name):
        return ''
    with open(file_name, 'r') as rf:
        return rf.read()

def load_json(file_name):
    with open(file_name, 'r') as rf:
        return json.load(rf)

def copy_json(obj):
    return json.loads(json.dumps(obj))

def get_this_ip(url="http://api.xunliansoft.com/api/ApiHub/hello", default="127.0.0.1", f=lambda o, d: o.get("ip", d)):
    try:
        res = requests.get(url)
        if res.ok:
            o = res.json()
            return f(o, default)
    except Exception as ex:
        print "get_this_ip with error", repr(ex)

    return default

class Api(object):
    def __init__(self, config):
        # 创建 AcsClient 实例
        self.client = AcsClient(
            config.get("accessKeyId", ""),
            config.get("secretAccessKey", ""),
            config.get("regionId", ""),
        )
        self.config = copy_json(config)

    def apiDescribeDBInstances(self, dBInstanceId):
        client = self.client
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_DBInstanceId(dBInstanceId)
        response = client.do_action_with_exception(request)
        ret = json.loads(response)
        Items = ret.get("Items", {}) if ret else {}
        DBInstance = Items.get("DBInstance", []) if Items else []
        info = DBInstance[0] if DBInstance else None
        return info

    def apiDescribeDBInstanceAttribute(self, dBInstanceId):
        client = self.client
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_DBInstanceId(dBInstanceId)
        response = client.do_action_with_exception(request)
        ret = json.loads(response)
        Items = ret.get("Items", {}) if ret else {}
        DBInstanceAttribute = Items.get("DBInstanceAttribute", []) if Items else []
        info = DBInstanceAttribute[0] if DBInstanceAttribute else None
        return info

    def apiDescribeDBInstanceIPArrayList(self, dBInstanceId):
        client = self.client
        request = DescribeDBInstanceIPArrayListRequest.DescribeDBInstanceIPArrayListRequest()
        request.set_DBInstanceId(dBInstanceId)
        response = client.do_action_with_exception(request)
        ret = json.loads(response)
        Items = ret.get("Items", {}) if ret else {}
        DBInstanceIPArray = Items.get("DBInstanceIPArray", []) if Items else []
        info = DBInstanceIPArray if DBInstanceIPArray else []
        return info

    def apiModifySecurityIpsRequest(self, dBInstanceId, iPArrayName, ip, modifyMode="Append", whitelistNetworkType="Classic"):
        client = self.client
        request = ModifySecurityIpsRequest.ModifySecurityIpsRequest()
        request.set_DBInstanceId(dBInstanceId)
        request.set_SecurityIps(ip)
        request.set_WhitelistNetworkType(whitelistNetworkType)
        request.set_DBInstanceIPArrayName(iPArrayName)
        request.set_ModifyMode(modifyMode)
        response = client.do_action_with_exception(request)
        ret = json.loads(response)
        return ret

def main():
    configs = load_json( cwd('rds_config.ignore') )
    for config in configs:
        append_rds_ip(config)

def append_rds_ip(config):
    dBInstanceId = config.get("dBInstanceId", "")
    iPArrayName = config.get("iPArrayName", "")

    if not dBInstanceId or not iPArrayName or \
        not config.get("accessKeyId", "") or \
        not config.get("secretAccessKey", "") or \
        not config.get("regionId", ""):
        print _T('error'), "config error, config:", repr(config)
        return

    ip = get_this_ip()
    print _T(), "this ip:", ip
    if not ip or ip == "127.0.0.1":
        print _T('error'), "get ip, ip", ip
        return

    print _T(), "load config:", json.dumps(config, indent=2)
    api = Api(config)

    info = api.apiDescribeDBInstances(dBInstanceId) if dBInstanceId else None
    attr = api.apiDescribeDBInstanceAttribute(dBInstanceId) if dBInstanceId else None
    if not info or not attr:
        print _T('error'), "get rds info dBInstanceId:", dBInstanceId
        return

    info.update(attr)
    print _T(), "rds info:", json.dumps(info, indent=2)

    ips = api.apiDescribeDBInstanceIPArrayList(dBInstanceId)
    print _T(), "rds ips:", json.dumps(ips, indent=2)

    ipa_ = filter(lambda o: o.get("DBInstanceIPArrayName", "") == iPArrayName, ips)
    ipa = ipa_[0] if ipa_ else None
    if not ipa:
        print _T('error'), "get rds ipa iPArrayName:", iPArrayName
        return

    print _T(), "rds ipa:", json.dumps(ipa, indent=2)
    ips = set(ipa.get("SecurityIPList", "").split(","))

    if ip in ips:
        print _T(), "skip with this ip:", ip, " in ips:", ",".join(ips)
        return

    print _T(), "try add ip:", ip, " to:", ips

    ret = api.apiModifySecurityIpsRequest(dBInstanceId, iPArrayName, ip)
    print _T(), "added ret:", ret

def _T(tag = 'INFO'):
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return '%s [%s] => ' % (time_str, tag.upper())
        
if __name__ == '__main__':
    main()
