FROM python:3.10-slim

WORKDIR /app

COPY code/consumer.py ./
COPY code/.env ./
COPY requirements.txt ./

RUN set -x \
    # create nginx user/group first, to be consistent throughout docker variants
    && adduser --system --disabled-password --no-create-home emile \
    && apt-get update \
    && pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt


RUN chown -R emile /app
USER emile

CMD ["python", "consumer.py"]
