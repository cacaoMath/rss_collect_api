FROM python:3.10.8-slim

RUN apt update \
    && apt install -y sudo mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file \
    && cd /tmp/ \
    && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd \
    && echo yes | ./bin/install-mecab-ipadic-neologd -n


