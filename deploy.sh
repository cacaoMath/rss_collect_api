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
docker run -v dic:/dic --name mycontainer -p 8000:8000 deployimg