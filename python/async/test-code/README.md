# async的一些测试代码

## 异步队列
    PYTHONPATH=. python3 aqueue/main.py

## 取消coroute
    PYTHONPATH=. python3 cancel/main.py
    PYTHONPATH=. python3 cancel/main1.py
    PYTHONPATH=. python3 cancel/main2.py

## condition
    PYTHONPATH=. python3 condition/main.py

## create task
    PYTHONPATH=. python3 ctask/main.py
    PYTHONPATH=. python3 ctask2/main.py

## echo server
    PYTHONPATH=. python3 echo_server/main.py

## event
    PYTHONPATH=. python3 event/main.py

## gather
    PYTHONPATH=. python3 gather/main.py

## hello
    PYTHONPATH=. python3 hello/main.py

## lock
    PYTHONPATH=. python3 lock/main.py

## muti process
    cd mp
    bash data_set.sh
    cd ..

    PYTHONPATH=. python3 mp/main.py
    PYTHONPATH=. python3 mp/map_reduce.py

## muti thread
    PYTHONPATH=. python3 mt/main.py

## semaphore
    PYTHONPATH=. python3 semaphore/main.py