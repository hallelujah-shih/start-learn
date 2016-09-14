#!/bin/bash

# 根据自己的需要调整相关参数
export ES_HEAP_SIZE=4g
export MAX_LOCKED_MEMORY=unlimited
exec setuidgid app /srv/elasticsearch-2.3.2/bin/elasticsearch
