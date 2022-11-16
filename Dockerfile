FROM python:3.10.8-slim

COPY ./img_setup.sh /img_setup.sh
COPY ./Pipfile /Pipfile
COPY ./app /app
COPY ./dic /dic
COPY ./.env /.env

RUN ["/img_setup.sh"]

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

