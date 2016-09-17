import os
import rsa
import json
import random
import base64
import time

from app import app, server
from flask import render_template, session, request

def init_task_id(expiry_sec=app.config['TASK_ID_EXPIRY_SEC']):
    task_uptime = session.get('task_uptime', 0) if session.get('task_uptime', 0)!=-1 else time.time()
    if not session.get('task_id', '') or time.time()>task_uptime+expiry_sec:
        tmp = ''.join([random.choice('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678') for _ in range(16)])
        session['last_id'] = session.get('task_id', tmp)
        session['task_id'] = tmp
        session['task_uptime'] = int(time.time())
    return session['task_id'], session['task_uptime'], session['last_id']

def init_task_key(keytime, key, expiry_sec=app.config['TASK_ID_EXPIRY_SEC']):
    if time.time()>keytime+expiry_sec or not key:
        return False

    session['task_uptime'] = -1
    session['task_keytime'] = keytime
    session['task_key'] = key
    return True

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/testPage')
def testPage():
    init_task_id()
    rand_key = random.choice(server.client_pem.keys())
    return render_template("testPage.html",
        server = server,
        rand_key = rand_key,
        session = session)

@app.route('/testInfo')
def testInfo():
    init_task_id()
    tmp = dict(session)
    tmp['uptime'] = int(time.time())
    return json.dumps( tmp )

@app.route('/serverInfo')
def serverInfo():
    data = {
        'errno': 0,
        'pubkey_n': str(server.pubkey.n),
        'pubkey_e': str(server.pubkey.e),
        't': int(time.time())
    }
    return json.dumps(data)

@app.route('/getTaskToken')
def getTaskToken():
    task_id, task_uptime, _ = init_task_id()
    if task_uptime==-1:
        return json.dumps({'errno': 702, 'error': 'error task has saved.'})

    pubkey_n = request.args.get('pubkey_n', 0)
    pubkey_e = request.args.get('pubkey_e', 0)

    if pubkey_n and pubkey_e and task_id:
        client_pubkey = rsa.PublicKey( long(pubkey_n), long(pubkey_e) )
        data = {
            'errno': 0,
            'id':  base64.b64encode(rsa.encrypt(task_id, client_pubkey)),
            'up_time': task_uptime,
            'expiry_sec': app.config['TASK_ID_EXPIRY_SEC'],
            't': int(time.time())
        }
        return json.dumps(data)
    else:
        return json.dumps({'errno': 803, 'error': 'error client pubkey_n or pubkey_e.'})

@app.route('/sendData')
def sendData():
    task_id, task_uptime, last_id = init_task_id()
    if task_uptime==-1:
        return json.dumps({'errno': 701, 'error': 'already task has saved.'})

    data = request.args.get('data', '')
    task = {}

    try:
        data = base64.urlsafe_b64decode( str(data) )
        task_json = rsa.decrypt(data, server.privkey)
        task = json.loads(task_json) if task_json else {}
    except TypeError as ex1:
        return json.dumps({'errno': 501, 'error': 'error base64.urlsafe_b64decode.'})
    except rsa.DecryptionError as ex2:
        return json.dumps({'errno': 502, 'error': 'error rsa.decrypt.'})
    except ValueError as ex3:
        return json.dumps({'errno': 503, 'error': 'error json.loads.'})
    except Exception as ex_all:
        return json.dumps({'errno': 504, 'error': 'error Exception.'})

    if task_id and (task_id==task.get('id', '') or last_id==task.get('id', '')) and init_task_key(task.get('t', 0), task.get('k', '')):
        return json.dumps({'errno': 0, 'sucess': 'save task done.'})
    else:
        return json.dumps({'errno': 601, 'error': 'error input task.'})

