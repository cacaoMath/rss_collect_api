#!bin/bash
if [ -z "$(echo `mecab-config`)" ]; then
    echo "mecabなどが入っていないのでインストールしてください"
    exit 0
fi
MECAB_DIC_PATH=$(echo `mecab-config --dicdir`"/mecab-ipadic-neologd")

if [ -z "$(ls ${MECAB_DIC_PATH}/)" ]; then
    echo "ipadic-neologd辞書がありませんインストールしてください"
    exit 0
else
    if [ ! -d ./dic ]; then
        mkdir dic
    fi
    if [ -z "$(ls ./dic)" ]; then
        cp -r ${MECAB_DIC_PATH} ./dic
    fi
fi
echo "MECAB_DIC_PATH=/dic/mecab-ipadic-neologd" > .env
docker build -t deployimg .
if [ -n "$(echo `docker ps | grep deployimg`)" ]; then
    docker stop mycontainer
    docker rm mycontainer
fi
docker run -d --name mycontainer -p 8000:8000 deployimg 
