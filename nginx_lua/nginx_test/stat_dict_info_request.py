# -*- coding:utf-8 -*-
# !/user/bin/env python

__author__ = 'shih'

import urllib
import random
import requests


ip_weight = {
    '10.8.255.181': 0.5,
    '10.8.255.182': 0.3,
    '10.8.255.183': 0.2
}

ip_err_weight = {
    '10.8.255.181': 0.8,
    '10.8.255.182': 0.006,
    '10.8.255.183': 0.001
}

total_req = 10000


def gen_data(data_len, err_weight):
    return [200 if random.random() > err_weight else 500 for _ in xrange(data_len)]


def send_request(ip, data_list):
    session = requests.session()
    with session:
        for k in data_list:
            tmp = session.get('http://test.start-learn.win/?%s' % urllib.urlencode({'ip': ip, 'status': k}))
            if tmp.status_code == 200:
                continue
            else:
                print tmp.content
    print 'req ip:', ip, ' req status:', k, ' rt:', tmp.content

if __name__ == '__main__':
    ip_data = {k: gen_data(int(ip_weight[k] * total_req), ip_err_weight[k]) for k in ip_weight}
    for k, v in ip_data.iteritems():
        send_request(k, v)