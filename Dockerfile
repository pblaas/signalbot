FROM pblaas/signalcli:latest

LABEL MAINTAINER="patrick@kite4fun.nl"

USER root

RUN apt-get update && \
    apt-get -y install python3 python3-pip vim

RUN mkdir -p /tmp/signal && \
    chown nobody /tmp/signal

RUN mkdir /app && \
    chown -R nobody /app

COPY app/ ./app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN chown -R nobody /app

USER nobody

ENTRYPOINT ["python3", "app.py"]