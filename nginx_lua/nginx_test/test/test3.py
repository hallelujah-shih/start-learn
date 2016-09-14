# -*- coding:utf-8 -*-
# !/user/bin/env python

__author__ = 'shih'

import time
import math
import copy
import Queue
import random
import threading


def gen_random_datas(data_len, rate):
    for i in xrange(data_len):
        yield random.random()
        time.sleep(rate)


def sw_calc(sw, user_define_sw, access_rt, time_diff, rate):
    # add_rate = 0.01 + rate if access_rt else -0.03
    # dev_num = float(9 * max(time_diff, 1) + 1)
    #
    # new_sw = sw * (1 + add_rate / dev_num)
    # new_sw = min(new_sw, 100)
    # return new_sw
    if access_rt:
        add_rate = math.log(1 + rate * rate)
        #dev_num = float(9 * max(time_diff, 1) + 1)
        new_sw = sw + math.log10(1 + add_rate)
        #new_sw = min(new_sw, 100)
    else:
        new_sw = sw * 0.90
    return new_sw


def simulat_thread(init_sw, sw, er, dq, key, sw_lock, sp):
    last_time = time.time()
    data_queue = dq[key]
    assert isinstance(data_queue, Queue.Queue)
    while True:
        data = data_queue.get()
        if not data:
            break

        access_rt = False if random.random() < er[key] else True
        now = time.time()
        new_sw = sw_calc(sw[key], init_sw[key], access_rt, now - last_time, sp[key])
        with sw_lock:
            sw[key] = new_sw
        last_time = now


def choice_channel(value, sw, sw_lock):
    with sw_lock:
        sorted_keys = sorted(sw.keys())
        total = 0
        for k in sorted_keys:
            total += sw[k]

        tmp_value = 0
        for k in sorted_keys:
            tmp_value += float(sw[k])
            if value < (tmp_value / total):
                return k


def get_new_sw(init_sw, sw, dq, err_rate, total_access, sw_lock, sp):
    thread_pool_st = []
    for k in init_sw:
        t = threading.Thread(target=simulat_thread, args=(init_sw, sw, err_rate, dq, k, sw_lock, sp))
        t.start()
        thread_pool_st.append(t)

    for d in gen_random_datas(total_access, 1.0/ total_access):
        k = choice_channel(d, sw, sw_lock)
        dq[k].put(d)

    for k in init_sw:
        dq[k].put(None)
    for t in thread_pool_st:
        t.join()


def test1():
    init_src_weight = {
        'a1': 50,
        'a2': 30,
        'a3': 20
    }

    speed_rate = {
        'a1': 0.0125,
        'a2': 0.017,
        'a3': 0.01
    }

    err_rate = {
        'a1': 0.003,
        'a2': 0.0005,
        'a3': 0.001
    }

    input_data_queue = {
        'a1': Queue.Queue(),
        'a2': Queue.Queue(),
        'a3': Queue.Queue()
    }

    sw = copy.deepcopy(init_src_weight)
    sw_lock = threading.Lock()
    print sw
    get_new_sw(init_src_weight, sw, input_data_queue, err_rate, 100, sw_lock, speed_rate)
    print sw
    get_new_sw(init_src_weight, sw, input_data_queue, err_rate, 1000, sw_lock, speed_rate)
    print sw
    get_new_sw(init_src_weight, sw, input_data_queue, err_rate, 100, sw_lock, speed_rate)
    print sw
    get_new_sw(init_src_weight, sw, input_data_queue, err_rate, 10000000, sw_lock, speed_rate)
    print sw

    err_rate = {
        'a1': 1,
        'a2': 0.0005,
        'a3': 0.001
    }

    speed_rate = {
        'a1': 0.0125,
        'a2': 0.1,
        'a3': 0.01
    }

    get_new_sw(init_src_weight, sw, input_data_queue, err_rate, 10000, sw_lock, speed_rate)
    print sw

test1()