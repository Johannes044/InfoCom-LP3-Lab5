#!/usr/bin/env bash

killall python
killall python3
killall Python
killall Python3

redis-cli flushall
redis-cli shutdown