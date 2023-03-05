FROM python:3.10-slim

WORKDIR /app

COPY drink_n_talk/requirements.txt .

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY drink_n_talk/ .

CMD ["gunicorn","drink_n_talk.wsgi:application","--bind","0:8000"]
