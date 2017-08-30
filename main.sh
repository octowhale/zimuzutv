#!/bin/bash
#

cd $(dirname $0)


kill -15 $(ps -ef |grep "python main.py" | awk '{print $2}')
git pull

sleep 2
python main.py &
