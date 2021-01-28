FROM pblaas/signalcli:latest

LABEL MAINTAINER="patrick@kite4fun.nl"

USER root

RUN apt-get update && \
    apt-get -y install python3 python3-pip vim

RUN mkdir -p /tmp/signal && \
    chown nobody /tmp/signal

RUN mkdir /app && \
    chown -R nobody /signalbot

COPY signalbot/ ./signalbot/
RUN pip install -r requirements.txt
RUN chown -R nobody /signalbot

USER nobody

ENTRYPOINT ["python3", "/signalbot"]