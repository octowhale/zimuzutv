#!/bin/bash
#

cd $(dirname $0)

git pull

[ $? -eq 0 ] || exit 1
kill -15 $(ps -ef |grep "python main.py" |grep -v "$0|grep" | awk '{print $2}')

sleep 2
python main.py &
