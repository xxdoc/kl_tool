import os
from flask import Flask
from base import BaseServer

app = Flask(__name__)
app.config.from_object('config')

server = BaseServer(app.config['SERVER_PUB_PEM'], app.config['SERVER_PRIV_PEM'], app.config['CLIENT_PEM_PATH'])

from app import views