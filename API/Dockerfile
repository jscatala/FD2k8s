FROM python:3.10-slim

WORKDIR /app

COPY code/api.py ./
COPY code/producer.py ./
COPY requirements.txt ./

RUN set -x \
    # create nginx user/group first, to be consistent throughout docker variants
    && adduser --system --disabled-password --no-create-home emile \
    && apt-get update \
    && pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt


RUN chown -R emile /app
USER emile

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8800"]
