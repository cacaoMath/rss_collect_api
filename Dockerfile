FROM python3.10.8_with_mecab:latest

COPY ./Pipfile.lock /Pipfile.lock
COPY ./app /app
COPY ./.env /.env

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv sync

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

