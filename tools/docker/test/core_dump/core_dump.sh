#!/bin/bash

echo "/tmp/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

g++ -g -O0 -o /tmp/core_dump core_dump.cpp

cd /tmp && ./core_dump
