FROM python3.10

COPY ./setup.sh ./setup.sh

RUN ["setup.sh"]

EXPOSE 8000

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

