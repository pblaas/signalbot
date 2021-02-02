FROM pblaas/signalcli:latest

LABEL MAINTAINER="patrick@kite4fun.nl"


ENV REGISTEREDNR=""
ENV DEBUG=""
ENV SIGNALEXECUTORLOCAL=""
ENV READY=""
ENV GIPHY_APIKEY=""
ENV GNEWS_APIKEY=""
ENV TWITCH_CLIENTID=""
ENV TWITCH_CLIENTSECRET=""


USER root

RUN apt-get update && \
    apt-get -y install python3 python3-pip vim

RUN mkdir -p /tmp/signal && \
    chown nobody /tmp/signal

RUN mkdir /signalbot && \
    chown -R nobody /signalbot

COPY signalbot/ ./signalbot/
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN chown -R nobody /signalbot

USER nobody

ENTRYPOINT ["python3", "/signalbot"]