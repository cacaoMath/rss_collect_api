FROM python:3.10.8-slim

COPY ./deploy_setup.sh /deploy_setup.sh
COPY ./Pipfile.lock /Pipfile.lock
COPY ./app /app
COPY ./dic /dic
COPY ./.env /.env

RUN ["/deploy_setup.sh"]

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

