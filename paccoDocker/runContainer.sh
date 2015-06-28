#!/bin/sh

echo "Clean all stopped containers"
docker stop $(docker ps -a -q)
#docker rm $(docker ps -a -q -f status=exited)

docker run -t -i -p 5002:80 -v /mnt/eos-share:/mnt/eos-share paccotest /bin/bash
