#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import socket
import time

def monitor_port(protocol, port, cmd):
    address = ('127.0.0.1', port)
    socket_type = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM
    client = socket.socket(socket.AF_INET, socket_type)

    try:
        client.bind(address)
    except Exception as e:
        print 'running...'
        pass
    else:
        sys.stderr.write('port[%s-%s] is lost, run [%s]\n' % (protocol, port, cmd))
        print 'start...'
        client.close()
        time.sleep(1)
        os.system(cmd)
    finally:
        client.close()


def main():
    monitor_port('udp', 6881, './run.sh')

# using example
if __name__ == "__main__":
    main()
