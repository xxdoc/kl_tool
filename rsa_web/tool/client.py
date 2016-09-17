import rsa
import base64
import json
import time

pubkey = rsa.PublicKey.load_pkcs1_openssl_pem('''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2STrRJjnVw1UJUGUIaYC6GM3x
qJvvbSHMGZvXPbUQqhHktgIb6rmlFsMhCVxOu3DUiKtRLrHa4Q0HzX+VYO3ulCYZ
FTXYiJi7E7U8dLF7E7fADIlWKZbr7fzir0/2cMOBzLQCYgq9hU/LjkY8cjIKvyQ9
8pNnbAFnkb6Mu+2rQQIDAQAB
-----END PUBLIC KEY-----''')

privkey = rsa.PrivateKey.load_pkcs1('''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQC2STrRJjnVw1UJUGUIaYC6GM3xqJvvbSHMGZvXPbUQqhHktgIb
6rmlFsMhCVxOu3DUiKtRLrHa4Q0HzX+VYO3ulCYZFTXYiJi7E7U8dLF7E7fADIlW
KZbr7fzir0/2cMOBzLQCYgq9hU/LjkY8cjIKvyQ98pNnbAFnkb6Mu+2rQQIDAQAB
AoGARZl6Uqc0x/C4BEFlAiw+UU/tOkr1lxplICfa//j4rG8zO89eyMf7sBQb1v5a
91jMQOoZ93pLwFXTgtosz51d2ueSIdbxHqhfP1rv3yfVhK6LDiwVNDWAoBhPatik
xHEH7w2CjC8OUAfFYqlTkG57oWneh/C4RmQoIJVi1FDrAi0CQQDtl9qOTe+uWskR
bS4qon94AOqQlM3cP7vBODK2k/u5JsAsOWFTB6SyQryqlzq3uzCp+0qRZLjY5On6
HLg3ZVWDAkEAxGh6nEcrsbL50B5a4OQ0Fzh1WJBSIlfWOmvAVGeBKNH2/C4LzGVK
DZtMwbc8EA1/k+hDv6EB8xRB8/V/uqtk6wJABQoJeqcwhDQsu4/jQMg9h+ANGY/u
ZdN8OfblLHYrCpxFyypUZBxvY9CCi+O1PRxdRd2skTTfrsn8JG/jgFlH3QJBALBu
Rg3SZO64nm2UhwBUHnLpdYf8BLvy+W77Uga//6cijWJVHqYaKt50LgwpxFuLNJox
34HpaS3peaFjW7zcr8cCQQCSfLeudro+WyiKRBs/pVsR4WV5AFlYZIDe/MvCsx6b
JCdhNmlgP7/qebLPOClooTN+99+gMDTa5Hzqurp28jSj
-----END RSA PRIVATE KEY-----''')


def main():
    server_info = {
        "errno": 0,
        "pubkey_n": "117031647389468154238294760221768669666720727567321559438674532881383123833991837204444674701824886690302799348724838187836113927017307648768874827857745750096232380907604343230843940979123293616378389630394012315456891843867983730497700603209106315098130010818372297137065561806160237509869074384439104806477",
        "pubkey_e": "65537",
        "t": 1474101614
    }
    server_pubkey = rsa.PublicKey( long(server_info['pubkey_n']), long(server_info['pubkey_e']) )

    print 'pubkey_n:', pubkey.n
    print 'pubkey_e:', pubkey.e
    print 'http://127.0.0.1:5000/getTaskToken?pubkey_n=%s&pubkey_e=%s' % (pubkey.n, pubkey.e)

    task_token = "lwXLvE2nWtouITCyZ+G4LUWNezydEQClU3aUYqKprmdmCk18hjjk9ZbcDM3/+WoodE8oESPvuShavdzoB6tkXl6L2IWV1Ljj1QoQ4qkbrqasz1HTeiBCsoeFhVywNlVFcP5vBTzQvnbFAJEKwWHQTjw3csv6VQ8A5lLPPzIL4AY="

    task_id = rsa.decrypt(base64.b64decode(task_token), privkey)
    print '\n','task_token:', task_token
    print 'task_id:', task_id

    data_json = json.dumps({
        'id': task_id,
        't': int(time.time()),
        'k': 'key cannot too long, less than 64 charts, use key to AES or DES.',
    })

    data_crypt = base64.urlsafe_b64encode( rsa.encrypt(data_json, server_pubkey) )
    print 'http://127.0.0.1:5000/sendData?data=%s' % (data_crypt)

if __name__ == "__main__":
    main()

