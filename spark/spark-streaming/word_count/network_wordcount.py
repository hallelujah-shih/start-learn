#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
 Counts words in UTF8 encoded, '\n' delimited text received from the network every second.
 Usage: network_wordcount.py <hostname> <port>
   <hostname> and <port> describe the TCP server that Spark Streaming would connect to receive data.

 To run this on your local machine, you need to first run a Netcat server
    `$ nc -lk 9999`
 and then run the example
    `$ bin/spark-submit examples/src/main/python/streaming/network_wordcount.py localhost 9999`
"""
from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def update_count(new_counts, old_stat):
    if not isinstance(old_stat, dict):
        old_stat = {}
    old_stat['calc_count'] = 1 + old_stat.get('calc_count', 0)
    old_stat['sum_key'] = sum(new_counts) + old_stat.get('sum_key', 0)
    return old_stat


def create_context(host, port):
    print("create new context")
    sc = SparkContext(appName="world_count")
    ssc = StreamingContext(sc, 5)
    lines = ssc.socketTextStream(host, port)
    words = lines.flatMap(lambda line: line.split(" "))
    word_counts = words.map(lambda x: (x, 1)).updateStateByKey(update_count)

    word_counts.pprint()
    return ssc

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: network_wordcount.py <hostname> <port>", file=sys.stderr)
        exit(-1)
    host, port = sys.argv[1], int(sys.argv[2])
    checkpoint = "checkpoint"

    ssc = StreamingContext.getOrCreate(checkpoint, lambda: create_context(host, port))

    ssc.start()
    ssc.awaitTermination()
