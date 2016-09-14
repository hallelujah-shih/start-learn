# -*- coding:utf-8 -*-
# !/user/bin/env python

__author__ = 'shih'


import json


host_info_set = {
    'test.start-learn.win': {
        'origin_server': [{'host': '122.114.45.153', 'port': 80, 'scheme': 'http', 'weight': 50, 'active': True},
                          {'host': '122.114.45.153', 'port': 8080, 'scheme': 'http', 'weight': 30, 'active': True},
                          {'host': '122.114.45.153', 'port': 8000, 'scheme': 'http', 'weight': 20, 'active': True}]
        }
    }


host_info_set = {
    'test.start-learn.win': {
        'origin_server': [{'host': '10.8.255.70', 'port': 80, 'scheme': 'http', 'weight': 50, 'active': True},
                          {'host': '10.8.255.70', 'port': 8080, 'scheme': 'http', 'weight': 30, 'active': True},
                          {'host': '10.8.255.70', 'port': 8000, 'scheme': 'http', 'weight': 20, 'active': True}]
    }
}


if __name__ == '__main__':
    with open('host_info.json', 'w') as f:
        json.dump(host_info_set, f)