#!bin/bash

# docker build & run
docker build -t python3.10.8_with_mecab ./dockerfile/neologd
docker build -t app_deploy .
if [ -n "$(echo `docker ps -a | grep rss_api`)" ]; then
    docker stop rss_api
    docker rm rss_api
fi
docker run -it -d --name rss_api -p 8000:8000 --add-host=gateway.docker.internal:host-gateway app_deploy
