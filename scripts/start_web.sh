#!/usr/bin/env bash

source venv/bin/activate
cd src/webserver

redis-server &
python3 database.py &
python3 route_planner.py &
python3 build.py &
