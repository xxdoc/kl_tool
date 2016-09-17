import os

SECRET_KEY = 'you-will-never-guess'

TASK_ID_EXPIRY_SEC = 10
CLIENT_PEM_PATH = os.path.join(os.getcwd(), 'pem')
SERVER_PUB_PEM = os.path.join(CLIENT_PEM_PATH, 'www_pub.pem')
SERVER_PRIV_PEM = os.path.join(CLIENT_PEM_PATH, 'www_priv.pem')