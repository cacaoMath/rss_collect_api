#!/usr/bin/env bash
apt update
apt install -y mecab libmecab-dev mecab-ipadic-utf8
pip install --upgrade pip
pip install fastapi uvicorn
pip install pipenv
pipenv install