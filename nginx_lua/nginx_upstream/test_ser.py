#-*- coding:utf-8 -*-
#!/user/bin/env python

__author__ = 'shih'

import gevent 
from gevent.server import StreamServer


# this handler will be run for each incoming connection in a dedicated greenlet
def echo(socket, address):
    num = 0
    while True:
        try:
            if num and num % 3 == 0:
                print socket.recv(4)
                gevent.sleep(3)
                break
            else:
                content = "%0100d" % num
                line = socket.recv(4096)
                if not line:
                    break

                print line
                socket.send("HTTP/1.1 200 OK\r\nDate: Mon, 24 Oct 2016 11:05:48 GMT\r\nContent-Type: text/html; charset=GBK\r\nContent-Length: 100\r\nConnection: keep-aliver\r\nVary: Accept-Encoding\r\n\r\n")
                gevent.sleep(3)
                socket.send(content)
        except Exception as e:
            print e
            break
        num += 1
    socket.close()

if __name__ == '__main__':
    # to make the server use SSL, pass certfile and keyfile arguments to the constructor
    server = StreamServer(('0.0.0.0', 80), echo)
    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    server.serve_forever()
