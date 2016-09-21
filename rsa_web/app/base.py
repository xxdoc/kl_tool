import os
import rsa
import collections

RsaKeyPem = collections.namedtuple('RsaKeyPem','pub_pem pubkey priv_pem privkey')

class BaseServer(object):
    def __init__(self, pub, priv, root):
        with open(os.path.join(root, pub), 'r') as rf:
            self.pub_pem = rf.read()
            self.pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(self.pub_pem)
        with open(os.path.join(root, priv), 'r') as rf:
            self.priv_pem = rf.read()
            self.privkey = rsa.PrivateKey.load_pkcs1(self.priv_pem)

        self.client_pem = {}
        for item in os.listdir(root):
            tmp = item.split('_')
            if len(tmp)==2 and tmp[1]=='pub.pem' and tmp[0].isdigit() and \
                os.path.isfile(os.path.join(root, item)) and \
                os.path.isfile(os.path.join(root, tmp[0]+'_priv.pem')):

                with open(os.path.join(root, tmp[0]+'_priv.pem'), 'r') as rf:
                    priv_pem = rf.read()
                    privkey = rsa.PrivateKey.load_pkcs1(priv_pem)
                with open(os.path.join(root, tmp[0]+'_pub.pem'), 'r') as rf:
                    pub_pem = rf.read()
                    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(pub_pem)
                self.client_pem.setdefault(tmp[0], RsaKeyPem(pub_pem=pub_pem, pubkey=pubkey, priv_pem=priv_pem, privkey=privkey))
