#!/usr/bin/env python
# encoding: utf-8

import socket
import datetime
import pymongo
import time

from hashlib import sha1
from random import randint
from struct import unpack
from socket import inet_ntoa
from threading import Timer, Thread

from collections import deque

from bencode import bencode, bdecode

BOOTSTRAP_NODES = (
    ("router.bittorrent.com", 6881),
    ("dht.transmissionbt.com", 6881),
    ("router.utorrent.com", 6881)
)
TID_LENGTH = 2
RE_JOIN_DHT_INTERVAL = 3
TOKEN_LENGTH = 2


def entropy(length):
    return "".join(chr(randint(0, 255)) for _ in xrange(length))


def random_id():
    h = sha1()
    h.update(entropy(20))
    return h.digest()


def decode_nodes(nodes):
    n = []
    length = len(nodes)
    if (length % 26) != 0:
        return n

    for i in range(0, length, 26):
        nid = nodes[i:i+20]
        ip = inet_ntoa(nodes[i+20:i+24])
        port = unpack("!H", nodes[i+24:i+26])[0]
        n.append((nid, ip, port))

    return n


def timer(t, f):
    Timer(t, f).start()


def get_neighbor(target, nid, end=10):
    return target[:end] + nid[end:]


class KNode(object):

    def __init__(self, nid, ip, port):
        self.nid = nid
        self.ip = ip
        self.port = port


class BaseLogger(object):
    _LOG_LEVEL_DICT = {'DEBUG':10, 'INFO':20, 'WARN':30, 'ERROR':40, 'FALAT':50}

    def log(self, msg, tag='DEBUG'):
        tag = tag.upper()
        log_filter = lambda obj, t: obj._LOG_LEVEL_DICT.get(t, 0)>=20
        if getattr(self, 'log_filter', log_filter)(self, tag):
            if getattr(self, 'logger', None):
                self.logger.log(msg, tag)
            else:
                time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                print '%s [%s] %s' % (time_str, tag, msg)


class DHTClient(Thread, BaseLogger):

    def __init__(self, max_node_qsize, logger=None):
        Thread.__init__(self)
        self.setDaemon(True)
        self.max_node_qsize = max_node_qsize
        self.nid = random_id()
        self.nodes = deque(maxlen=max_node_qsize)
        self.logger = logger

    def send_krpc(self, msg, address):
        try:
            self.ufd.sendto(bencode(msg), address)
            return True
        except Exception:
            return False

    def send_find_node(self, address, nid=None):
        nid = get_neighbor(nid, self.nid) if nid else self.nid
        tid = entropy(TID_LENGTH)
        msg = {
            "t": tid,
            "y": "q",
            "q": "find_node",
            "a": {
                "id": nid,
                "target": random_id()
            }
        }
        self.send_krpc(msg, address)

    def join_DHT(self):
        for address in BOOTSTRAP_NODES:
            self.send_find_node(address)

    def re_join_DHT(self):
        if len(self.nodes) == 0:
            self.join_DHT()
        timer(RE_JOIN_DHT_INTERVAL, self.re_join_DHT)

    def auto_send_find_node(self):
        wait = 1.0 / self.max_node_qsize
        while True:
            try:
                node = self.nodes.popleft()
                self.send_find_node((node.ip, node.port), node.nid)
            except IndexError:
                pass
            time.sleep(wait)

    def process_find_node_response(self, msg, address):
        nodes = decode_nodes(msg["r"]["nodes"])
        for node in nodes:
            (nid, ip, port) = node
            if len(nid) != 20: continue
            if ip == self.bind_ip: continue
            if port < 1 or port > 65535: continue
            n = KNode(nid, ip, port)
            self.nodes.append(n)


class DHTServer(DHTClient):

    def __init__(self, master, bind_ip, bind_port, max_node_qsize):
        DHTClient.__init__(self, max_node_qsize)

        self.master = master
        self.bind_ip = bind_ip
        self.bind_port = bind_port

        self.process_request_actions = {
            "get_peers": self.on_get_peers_request,
            "announce_peer": self.on_announce_peer_request,
        }

        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind((self.bind_ip, self.bind_port))

        timer(RE_JOIN_DHT_INTERVAL, self.re_join_DHT)


    def run(self):
        self.re_join_DHT()
        while True:
            try:
                (data, address) = self.ufd.recvfrom(65536)
                msg = bdecode(data)
                self.on_message(msg, address)
            except Exception as ex:
                #print 'run Exception:%s' % (ex, )
                pass

    def on_message(self, msg, address):
        #self.log('on_message msg:%s, address:%s' % (msg, address), 'DEBUG')
        if msg.get('y', '') == "r":
            if "nodes" in msg.get('r', {}):
                self.process_find_node_response(msg, address)
        elif msg.get('y', '') == "q":
            msg_q = msg.get("q", '')
            if msg_q in self.process_request_actions:
                self.process_request_actions[msg_q](msg, address)
            else:
                self.play_dead(msg, address)

    def on_get_peers_request(self, msg, address):
        self.log('get_peers msg:%s, address:%s' % (msg, address), 'DEBUG')

        infohash = msg.get("a", {}).get("info_hash", '')
        tid = msg.get("t", None)
        nid = msg.get("a", {}).get("id", None)
        if not infohash or tid is None or nid is None:
            return False

        token = infohash[:TOKEN_LENGTH]
        msg = {
            "t": tid,
            "y": "r",
            "r": {
                "id": get_neighbor(infohash, self.nid),
                "nodes": "",
                "token": token
            }
        }
        return self.send_krpc(msg, address)

    def on_announce_peer_request(self, msg, address):
        try:
            self.log('announce msg:%s, address:%s' % (msg, address), 'DEBUG')

            msg_a = msg.get('a', {})
            nid = msg_a.get("id", None)
            tid = msg.get('t', None)
            if nid is None or tid is None:
                return False

            infohash = msg_a.get("info_hash", '')
            token = msg_a.get("token", '')
            if not token or infohash[:TOKEN_LENGTH]!=token:
                self.log('announce error token:%s, infohash:%s' % (token, infohash), 'ERROR')
                return False

            if "implied_port" in msg_a and msg_a.get("implied_port", 0)!=0:
                port = address[1]
            else:
                port = msg_a.get("port", 0)
                if port < 1 or port > 65535: return

            from_addr = '%s:%s' % (address[0], port)
            return self.master.save(infohash.encode("hex"), from_addr)
        except Exception as ex:
            self.log('announce Exception:%s' % (ex, ), 'ERROR')
        finally:
            self.ok(msg, address)

    def play_dead(self, msg, address):
        tid = msg.get("t", None)
        if tid is None:
            return False

        msg = {
            "t": tid,
            "y": "e",
            "e": [202, "Server Error"]
        }
        return self.send_krpc(msg, address)

    def ok(self, msg, address):
        tid = msg.get("t", None)
        nid = msg.get("a", {}).get("id", None)
        if tid is None or nid is None:
            return False

        msg = {
            "t": tid,
            "y": "r",
            "r": {
                "id": get_neighbor(nid, self.nid)
            }
        }
        return self.send_krpc(msg, address)

class Master(BaseLogger):

    def __init__(self, mongo_host, mongo_port, database, collection, logger=None):
        self.con = pymongo.MongoClient(mongo_host, mongo_port)
        self.cur = self.con[database][collection]
        self.logger = logger
        self.cache = {}
        self.cache_time = 600

    def save(self, hash_key, from_addr):
        if not hash_key:
            return False

        time_now = int(time.time())
        if hash_key in self.cache:
            if time_now - self.cache[hash_key] > self.cache_time:
                self.cache[hash_key] = time_now
            else:
                #self.log('.', 'DEBUG')
                return False
        else:
            self.cache.setdefault(hash_key, time_now)

        time_per = time_now - 60
        per = len( [k for k, v in self.cache.items() if v > time_per] )
        msg = "<%d> %s from %s" % (per, hash_key, from_addr)
        self.log(msg, 'INFO')

        try:
            self.cur.update({'_id': hash_key}, {'$inc': {'count': 1}, '$set':{'uptime': time_now, 'try_count': 0}}, upsert=True)
            return True
        except pymongo.errors.PyMongoError as ex:
            msg = 'PyMongoError:%s, hash_key:%s, from_addr:%s\n' % (ex, hash_key, from_addr)
            self.log(msg, 'ERROR')
            return False

def main():
    # max_node_qsize bigger, bandwith bigger, speed higher
    mongo = Master('wownga.jios.org', 27017, 'btdb', 'magnet')
    dht = DHTServer(mongo, "0.0.0.0", 6881, max_node_qsize=400)
    dht.start()
    dht.auto_send_find_node()

# using example
if __name__ == "__main__":
    main()
