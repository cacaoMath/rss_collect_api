from dotenv import load_dotenv
import os

load_dotenv("./.env")

MECAB_DIC_PATH = os.environ.get("MECAB_DIC_PATH")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER")
POSTGRES_SERVER_PORT = os.environ.get("POSTGRES_SERVER_PORT")
AUTH_USER = os.environ.get("AUTH_USER")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD")
