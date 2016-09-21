import os
from flask import Flask
from base import BaseServer
import cPickle

app = Flask(__name__)
app.config.from_object('config')

if os.path.isfile( app.config['SERVER_OBJ_CPICKLE'] ):
    with open(app.config['SERVER_OBJ_CPICKLE'], 'r') as rf:
        server = cPickle.load(rf)
else:
    server = BaseServer(app.config['SERVER_PUB_PEM'], app.config['SERVER_PRIV_PEM'], app.config['CLIENT_PEM_PATH'])
    with open(app.config['SERVER_OBJ_CPICKLE'], 'w') as wf:
        cPickle.dump(server, wf)

from app import views