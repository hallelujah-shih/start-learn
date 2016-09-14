# -*- coding:utf-8 -*-
# !/user/bin/env python

__author__ = 'shih'

import time
import gevent.pool as pool
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

headers = {'Host': "test.start-learn.win"}
url = URL('http://10.8.150.240/')
# url = URL('http://10.8.150.241/')
http = HTTPClient.from_url(url, concurrency=50)

total = 0
ok = 0
err = 0
con_err = 0

def fetch_data(http, url, headers):
    global total, err, con_err, ok
    try:
        response = http.get(url.request_uri, headers=headers)
        if response.status_code != 200:
            err += 1
        else:
            ok += 1
        total += 1
        response.read()
    except Exception as e:
        con_err += 1
        pass

now = time.time()

p = pool.Pool(100)
for _ in xrange(100000):
    p.spawn(fetch_data, http, url, headers)
p.join()

http.close()

end = time.time()
print total, ok, err, con_err

print "used_time:", end - now