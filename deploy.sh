#!bin/bash
MECAB_DIC_PATH=$(echo `mecab-config --dicdir`"/mecab-ipadic-neologd")
if [ ! -d ./dic ]; then
    mkdir dic
fi
if [ -z "$(ls $directory)" ]; then
    cp -r ${MECAB_DIC_PATH=$(echo `mecab-config --dicdir`"/mecab-ipadic-neologd")} ./dic
fi
echo "MECAB_DIC_PATH=/dic" > .env
docker build -t deployimg .
if [ -n "$(echo `docker ps | grep deployimg`)" ]; then
    docker stop mycontainer
    docker rm mycontainer
fi
docker run -d -v dic:/dic --name mycontainer -p 8000:8000 deployimg