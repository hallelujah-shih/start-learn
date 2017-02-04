# /usr/bin/env python
# -*- coding:utf-8 -*-
from gevent.monkey import patch_all
patch_all()
from gevent.server import StreamServer
import gevent
import datetime


def handle(sock, address):
    while True:
        try:
            now = datetime.datetime.now()
            sock.sendall("%s\n" % now.strftime("%Y-%m-%d_%H:%M"))
            gevent.sleep(1)
        except Exception as e:
            sock.close()
            return


if __name__ == '__main__':
    ss = StreamServer(('', 9999), handle=handle)
    ss.serve_forever()
