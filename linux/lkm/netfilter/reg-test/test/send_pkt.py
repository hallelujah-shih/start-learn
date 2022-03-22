import socket


s = socket.socket()
s.bind(("127.0.0.1", 10240))
s.connect(("127.0.0.1", 10240))
