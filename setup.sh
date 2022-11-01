#!/usr/bin/env bash
apt-get update
apt-get install -y git
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
echo yes | ./bin/install-mecab-ipadic-neologd -n
MECAB_DIC_PATH=$(echo `mecab-config --dicdir`"/mecab-ipadic-neologd")
echo "MECAB_DIC_PATH=${MECAB_DIC_PATH}" > .env
cat .env
pip install fastapi uvicorn
pip install --upgrade pip
pip install pipenv
pipenv install