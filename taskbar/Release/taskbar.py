# -*- coding: utf-8 -*-
import gzip
import base64

EXE_CONFIG = {
    'szCommand': u'python',
    'szEnvironment': {
        'ENV_VISIBLE': u'0',
        'ENV_TOOLTIP': u'TaskBar',
        'ENV_TITLE': u'TaskBar Notify',
        'ENV_BALLOON': u'TaskBar 已经启动，单击托盘图标可以最小化。',
    },
    'szSubMenu': [
        {
            'Title': u'RunPython',
            'Cmd': u'python',
            'Path': u'C:\\Windows',
        },
        {
            'Title': u'记事本',
            'Cmd': u'notepad.exe',
            'Path': u'C:\\Windows',
        },
    ],
}

def main():
    #exe_buffer = getExeBuffer()
    #zip_buffer = zipExeBuffer(exe_buffer)
    exe_buffer = getExeBufferZip()
    idx = exe_buffer.find(unicode2wstr('python'))
    if(idx <=0 ): raise BufferError('cannot found tag in buffer')

    config = EXE_CONFIG
    len_list = [('szCommand', 1024), ('szEnvironment', 1024), ('szSubMenuTitle', 2048), ('szSubMenuCmd', 2048), ('szSubMenuPath', 2048), ]
    idx_map = {item[0]:(idx + 2 * sum([t[1] for t in len_list[:i]]), item[1]) for i, item in enumerate(len_list)}
    out_buffer = setWstrConfig(exe_buffer, idx_map, config)
    saveFile(out_buffer, 'test.exe')

def hexStrLine(bin_str, block_bytes = 2, line_blocks = 16):
    tmp_str, line_list, hex_list = '', [], ('%02x' % (ord(c), ) for c in bin_str)

    for idx, char in enumerate(hex_list, 1):
        tmp_str += char
        if idx % line_blocks == 0:
            line_list.append(tmp_str)
            tmp_str = ''
        elif idx % block_bytes ==0:
            tmp_str += ' '

    if tmp_str:
        line_list.append(tmp_str)
    return '\n'.join(line_list)

def saveFile(file_str, file_name):
    with open(file_name, 'wb') as wf:
        wf.write(file_str)

def setWstrConfig(exe_buffer, idx_map, config):
    config_map = fixExeConfig(config)
    out_buffer_list = [c for c in exe_buffer]
    for tag, (idx, slen) in idx_map.items():
        for i, c in enumerate(config_map.get(tag, '')):
            out_buffer_list[idx + i] = c

    return ''.join(out_buffer_list)

def fixExeConfig(config):
    for key in ['szCommand', 'szEnvironment']:
        if not config.get(key, ''):
            raise ValueError('cannot found key %s in config %r' % (key, config))

    config['szEnvironment'].update({'ENV_VISIBLE': u'0', 'ENV_TOOLTIP': u'TaskBar', 'ENV_TITLE': u'TaskBar Notify', 'ENV_BALLOON': u'TaskBar 已经启动，单击托盘图标可以最小化。',})
    return {
        'szCommand': unicode2wstr(config['szCommand']),
        'szEnvironment': unicode2wstr('\n'.join(['%s=%s' % (k, config['szEnvironment'][k]) for k in ['ENV_VISIBLE', 'ENV_TOOLTIP', 'ENV_TITLE', 'ENV_BALLOON',]]) + '\n'),
        'szSubMenuTitle': unicode2wstr('\n'.join([sub['Title'] for sub in config.get('szSubMenu', [])]) + '\n'),
        'szSubMenuCmd': unicode2wstr('\n'.join([sub['Cmd'] for sub in config.get('szSubMenu', [])]) + '\n'),
        'szSubMenuPath': unicode2wstr('\n'.join([sub['Path'] for sub in config.get('szSubMenu', [])]) + '\n'),
    }

def unicode2wstr(unicode_str):
    return ''.join([chr(ord(u)) + '\x00' if ord(u) < 256 else chr(ord(u)%256) + chr(ord(u)/256) for u in unicode_str])

def getExeBuffer():
    with open('taskbar.exe', 'rb') as rf: return rf.read()

def getExeBufferZip():
    return gzip.zlib.decompress(base64.decodestring(EXE_FILE_STR))

def zipExeBuffer(exe_buffer):
    return base64.encodestring(gzip.zlib.compress(exe_buffer, 9))

EXE_FILE_STR = '''
eNrtXQ10U8eVvhYGHDDBC1bjBKcRxCRpGxwXYxp+TGRsETuxjUBYspOAEJZkSZElRXrCkGKKK9Ti\nqN4mXQ79S7NQ0pT8tWw2P7T5c4HGaTdtOAt16DZNacsWsXYa2iTYSYHZ7857wnLA3W5Pztnt7rs+\n972ZuT9z752ZOyNhDw233UvjiCgXKATRPlLBTP81pIGXXvX9S+nJS34yc19O/U9mrvL5Y6ZINNwW\ndbWbWl2hUFgxrfOYovGQyR8y1Sy3mdrDbk/plCmTSjQd4+nmJ6tcHzuRwdLNV5+4Be/9ndeeMMv6\nnBPVeF+9eeGJZZLnuhOT8X548yxJ/1zbDfK90t/qY/mxbLVaiOpzcumZdz/XnGk7RlNzJudMgBOo\nKGqbYQYeBUCTFgUuG9T4EI28ae9IxSCfBSrv+ff5l4TFM4ncXNiJGOfRhwewsyxnbHKp4tnArj2X\nrxl0abYT51WsLY26XYqL6O8nar6zjdNG8yEa5lKVjTatxaMMWAO84gK+3tJoLNpKmq/wmSYB11yo\nj3T4H4Wm1GDX4B5kAPsL/HTYe5LNZ4QIkDX9SwzZruNRMyUO5nc/xa3dyTuYFuhLrsX705wyKtJg\n6Eu6Uec00mc5w5OxL+lDQyHmmTAeM5kpVZGLZ3cyiNae5CYhhI/iZrL2JTeg/Oxk8PWnOvOSQqlK\n9LCuQocwEkSSvZun9yQjaHFYRb+jJ7nhrBADl6tv3xbWIfp9FDOTyoWa6oBVxPOF8SBUBHKanWt+\ndOC8o9KlPsnEVdUnTShgyHItI/2jA4nBQluTvfxNR3ewpEAY89ijU6krC2aaqev3uZjhQ2/MOL1s\nwZzce800dWtSCheCuGAOoaW7pqRAiT3Pxb6aksIrEBXoKUrVlBT5tnzGTKJMGJtZ5TCaTEO/EmUz\nROLEcKIvTxifM8nwJ3uV8SkLDVyaPL1vX8RM8fH79kTYd6WkyIFHsTgsoDrxw1zWnOgkiu8sf1M1\nIjW86N19O1Wh7SzkM8KCJoc4jPYvqO1bZPtHtPYF8FIpAlVRqW6tq8JAgSrVrLbXSqnLRrSZ1fZ5\nsv1yrb2npqTYKoxFMKVJVHDwm6DrekaQjcXc3qRRhNHEYUP/qYoSlJQJYCvAwIt+OYyrb08cLDyA\nsXihzGzGZBXGx2Tg+nJLOGHZoS8fDXjtxevF3ggzpSqeREX0I45943kUOILJ3kDOauWjz/KQdf3J\nhGfn3zm6xwXIkjiQK/pbkr0t8ROJkseZn7S+1Y6tf13H3EVZ2UjHJbJj85gdmy7oeO1f1zF3saVj\npOMa2fHaMTs2Z3dsLz9t5yPBFoxDvt1utdrtPt4b5PL1FcAfWJSLkVr00m4ewDXxceW9B8CchyHP\nQ3tmXPNnyrXEnjwvjUxVso1NvrIbQX4tdWWRXFQtydMtyrWBSmh9EA1slDLZmzBRotdgtYvDTQFm\nlmzxn6cqCnmFTvSdQhe+krvY5cBNmmmy9iJONOSQ+cE3HOEWh0wavmOykn4CWSR9zTk8vobHCxwm\nH+cxO7oxFrDyO2DJHhTYhpYWu+8gCx7OhAcLNjcxbFAmJYZz11+WGJ7QMS1A+CnIuE2q2/tzOdEm\nBouhrYyHpuIrMivej6fvMZjqu1/au4ubE70mq287N269Sx3FImG8XtpQyZ6W7T6CZ3wycrQa44GJ\nKJyRycq3xMjdXidTZ7zA52MNxp0cyvLegUasKhR7LMetgXdEP6RMklGZm7Ic93Z1/o7yui1nOku8\nfZZzlCfiZzSuYlVdvm/xiDp4pWbVxOAqW/kvFqwumLr1VUR7weq8qVtfkoV8u5r3HfGpNmE0o2Tz\n0RZ2SY6RqDgiY/QOW15Q3tvS07m3z/IYHygCOW8/2txtOerttrzeYzll7bE8ZrVJEPEC6Fqsml0g\n4qfSTvC37H4dqgauBdV3XNq4nW1ssfme5JqUGeb+hfFGDn/8nVTlPC68Bg38yFMzcT8roG1yIvEQ\nDxjKe2/XvCxKVJZh8LHklJtSFbU8ULNlg8/N06+WfelPVdaYOFm+luzdfYxH6Urf9UwtklS07z6K\n0i4mwf6J6FgcGrhq11G1XhignoZ0oGgFph9TUpZhtoC3L7sjMD4TMHVdqeUzch6xty8qUc4D/aKC\nY5H+BM98mQJ8L8sNqZ79RRLPYNqMKQ+ydFTdHjmjeBPfomF8EnB8T2AnL+/ted6AKsx5+1Hvoz1J\npvk2RdlH4ymeS7IFlXvlTlUwdHRGr9MsQ3Z6/CD4cuKXbZkiC74HpcXXwfrdh1BMNWCC/KC2durW\nNvSUSF86dWsLCnNy8FDumjMO61CZs2gKs8YLeFmllw8J0dJy0gwGES/EWK3gMBmPo+uTc9DY1Vlo\nwGEcJC06aVDYIrN1oBTE8SBOTeZI8Tw1dmkTzD/5e0Ro6jPxgq5zvDfGrxo71icPgLXrHG+V8UsD\nlM3WdY63wnixnEByostJla5S43yyW0oWMc9lATV5yswkbeHZORDoOse7ZvzydOMQn8HUTHLk/MY4\nUNd1jo8Pm6q6zs3Cu2NBT+5TX3kLw7OXt4vUXt6txF7O4Pb0j5HbAjn29BWnufvCgSnp906zUmEc\nRF/lvWtW7y9Qs1JZypKX8LxOCc8xwpLlA1sgYO2zHCqTJ7oj6sHuaHMRzjKW47x6P4MlinJaGI/y\nsHvegYCIH++2DPZZTk2Q7MPsn+hHPumxHML8eB2MmYRRbE/F8xzd8uyY/o/3hLCnY3CiXDjs6Xve\nk9HCanCkX34fk403TZ/MzLxvp+/5E86CMomnze8Kkap4RU68QiQ1h4MPiZC8kjOcMB7Scp0wHuEs\n5GAW68AvnfD9R/D9FTF7H29BqcEAekF4fXuLzeTeJT8uurtn8zsx6LPZHd2edPkvulefCRic2Gjd\nnFoSUyIc68QUhV/C6ON1OCXIxz2MZlDWfLK2K8IV2r0BtfR8zL0FVx7kKZ3ve6iYB1Zhdek8EHz5\n7GoeHum30fcuN8tbtvdYtltFBW/YPZb7kQrvBe6EU5t488iVs4hFetncgyW7tnB3ZYvejk9PNJwR\nqYZT7u4p7IpzDTJZd/wL3sSSWXHLuCEupiZ4Fx1QJngrZ1H8TUkY/wGCida/2b36UI/lQfRoherT\nlkM5yvSpz1iODBRAwrT+sJQYeDswqdlqR4I2cmq0pqdj1ndbvgKprWyQZTCVl7qku2GbdUWaP4a2\ntBxIedIivk0YvwA6xmIb56fZG9gponH8yKH0dJUVZ4oDr0gQs9dKvjtM+kfHDwMOzSJ6HZgG0tVE\nxcC5wHqgF7gV+E3gE8AfA98A/h54Bshf4hQD5wGXAW8DbrpW1bvsGqIQyrcBa4ELgR8HXgGcAHwf\n9DTwDWA/8GVgL3AP8AHgDuA9wC3A9cAgcB3wNqAVOBe4+Bq1r2naexhL9jjwEHA/8DvACGz6LL+B\na4ArgWbgXGAxMB/4PngGga8Dfwp8DvgY8GvAe9gn4PbZah9IU6IN6/bTwJ0zR+K4rkT93iQ4a6Rt\nAux6BW3urLZr0HYQbcNZsk+irdmkj8+HMT6XjAvGlGjQE3Igichya2Qjyo6cmz2KbWNM8bTXeLyu\neFCpr67DUbOLLBsirpDbElrvj4ZD7Z6QYlOi/lBbzEGzWaYh7I4HPcv8QU+jq90DTZO4NYvd7or6\nXeuCILUabGNQHEypDodi4aDH1hr1eEJL416vJ2rz3+3BeNHNF6XWhbxhRERarrhrYWUQ3FVZuqrh\nqtoepT9kaXH4Q+5wB3/RVxUMhlu1VqIZVB0Mxzyaqk747les0XCrJxYjC1VHPS7Fo9Xh6RrZUzwa\nhS81/qinVQlHOZZL2CJmq3K7oyxK145EStUNrh0GW9DjidCtlpWNlvryuaXuYJDoH3Pqwy53XWsY\nA9RDNR4MUHhjgycUp1/lWMMxpQH6XG0sv8mwKupqvdMajsQjkoHOSA/j0Vg4ClasmYzF51nyqCoS\n8YTcXHHQfYamiBv0TDQCBpsv3JGp3aZJq3XLBgddDn9ZNmNBGfu/LBz1tEXD8ZBbEzyQo3EsDUPG\nyTwqZZVngwKpxw0dsQhmkOJ10DHp04q4P+MXfSmnLqay2/0xPyYHJREFr9rEMYWGHMNKT5sfUzWq\nNo9Y9E5OhlIddMVibDR9Q0ZUDYuDdlCNPxZxKa2+EanPciRDsSCczZhBpXLEMixNNsvKzAjdjU9p\nnmDQ2RhW/N6N6kjZai31mSH8qqHd0x7zKES/M3S0xrDUiH7Npdb2CNFbXFLCd/Ls8WIqE53McaLJ\nHY/QANOirb4oHZP8KNADBjVWmKsGZwckwhg/mp7j9IfXEb1r6NDIHwM1JpcvUYPNXr1ylWrtYXJ6\nMImplpzNrREF6xTBoTqDbKQT3He7OxjCAczp7GjzKO0uf8gVbcPsmYo+Qn4F7O2UABUuxWOouBSf\nJwrLvkFOlzsQjylOr9u/ng+8TmfE6WwNt/O/YRCF1bpXrXWpGpyuSMSpbIyg5cdsWasnojh96got\nJ3qGIB/ClA96EasV6sp2RZV4hNe643/BeUAhF8XoTlqHd/Qi9AhtBI8P3of0w5MOOuiggw46/D8B\nCzWSnZzAOrIBl1I92iqpjCadp62i5fipx7uOrKCt0s4US+WZIpuvDqjKj+YxgSOMc4afvDhvjEgs\npSrw10v9jReR+uPqVzffsGrPynzRZPvTiuZ1R9efs0/0vWX790Zqm3rHR2yGskn6EOqggw466KDD\nfxtWUhyf/K1Z3wJMor2pVOP1bfrOqoMOOuiggw466KCDDjrooIMO/1cgMuqTf0h+S+9Bq4vcVIrS\nBqD+TYAOOuiggw466KCDDjrooIMOOvxtQzUtpDvIQX589nfj038HxfB5/+KtOuiggw466KCDDjro\noIMOOuigw98m8O2uFtqAT/rahcn3vr+CXyvJQ0F88neptxzTT+7b6zn0xfptXLZRnNZRAzhCKBHd\nuOa6eOeq441Mq4UmNyhS1Y5Xkyq/T36HwLDEu3AjvxfLvwgMgXOJbD/6wIMpfk8iyvrrQP67wFUo\nWckhLyamMf5ykMb4W0W6yN8mjvU3j0RNIb7dxaSETTGPYmpVL1kxxeQNLqZ18goXU8x/t2fmpGxe\nfyimuIJBk3YrxEz+9oRtWk5N6JGvEeqgT8joqu11QPW27KjWbkEpimhEaSGZwOVCXNTfxDBpv4HR\nijjz72XM1GKgtlVTO2IdlN/SeMA7i2ZTDE8TeaHDD4oH9Jkypo2wpUZGrFR7E93WsSLuiW7kqyr4\nmgx/OJS5O4boVvSyElIWcJbT3CwpIu22GDDWudUxU78bytw1cafsOwg7boAl/IzIWWGCfSywatSd\nFNVAD0qKtDYzJ3X4MGCcvAv+OqItfE24GW++q60Z7w9mAY555CLtATy3jcG/8yLtfHvyvotkGW5/\n+aLZB2ufc8iDRL6se8x37iEqzOI8hc5qx13oYe24eXjasY55PfOc5RXN68wpV9oylBmez33rnNpf\nzqi+b9Jqufj54LzbY2AuG2ZmVK6xNmhTV1Udal6sUKKtkqfs/M88zGq+ZrFI9lANnnb8cKZUiNfV\nMpp+vj0iV/pGWOmSPCRzBWdK7ovXyDqMWRto6mouxZpnOYalNAV6MvbUAGOgsp0R+XfWmftcRt//\nYkI9jJ+gpM2nyVk67MAoeEdkP0nXQ6Js1JOhjPIgVyd9YpkQdAezvPjgnTOLKR/89aC1SU72nn/v\njK1tw97AObBB5mcTuPzwg+MVk7quk3EckV0FKZfcYdql9jtlVHlucx/LNZ1+zaaMb6ExbMv8hpt6\nRX4OdgyWX69lo6XIuizvlvoLNHoY9ThsVEaNW5v0iakb4JnpghgslLEeLf/BiI8Vb9U2G/Rz1vdL\nz7Jtq5F0u+zpwhlK2G1yZdaNyvkWA901ao4Q7c3lOBec78ukxjT3L0oy/D8CXAmskNMS24PcorCk\ngVdp9DHhpkN/qF9w+P1XbvjXs0PXHBKi+BUhLu97/+i0L/fype2L6IL/tWA0NL5xdqjmF0IsPCpE\n2REhWAfDjH85O6SmPCoGXkL8X1Ooi96g1fkuymnNvxWi8VdCSB2vQcdhIWZrdoBepfl1PfCjwMma\nPzPltAZt3QkhMjoq+9KPzPvhwMMf3z/w8MwXBh4uelbFaV9/aaOmy7Q7bg5/M1Y5dH9kIeu/NTgg\nRLaOatixAHbcADtKXlXtYJz2tf13g3/edzqrX9uzsUrsUirFrXOLbw//9t1/Zh0u6HBAR0OWjtIs\nHVf84O39bMMTXcuGHu+sEQ9tMIv72uY/wiEM/fqPDwVOnh1y/W5Ex1LouDFLhxbPm7/3+VvEE103\ni0c3VYtvrb9J/IN//tOWT864A7R6efxTx7/KcuA3d1b9/OwQ65gDHVe/KuO57IVUg3gmWSf2blkm\nHvn0UrE7vkTcH1kkdgQ+Jbb754sv+SqGPr927tPgXW756eC2pf8mxKf6VR1oqzzwRat4rrtePLW1\nVnz3MxaRicXXwwulfAY1HdW3viFEFXTM/9nZN3kpvHTfyud/0LNcPLvtVvFkolZkYrEzVim+2r5g\nlA72p+k3Qtzyy7NDS3723me14ykd/GLj5hfvqd/5dLJ21+Od1bvR/7d3BBc8cq93/iNfDt44Sl7b\nCsYEjsU/ZcXiG1mx0OaM8c/JP3dPvZzvmVh8U1lyPhZa+pz85+R7exq/+/3P3fKmjMXmGvFtxOKB\nuxYP7fB96kua7Khd99REDf/CE8iWiVkyEzNnh4ICNcvwjq+f9j5M+E+xnGYp
'''

if __name__ == '__main__':
    main()