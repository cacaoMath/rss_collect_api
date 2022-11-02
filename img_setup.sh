#!/usr/bin/env bash
apt-get update
apt-get install -y mecab libmecab-dev mecab-ipadic-utf8
pip install fastapi uvicorn
pip install --upgrade pip
pip install pipenv
pipenv install