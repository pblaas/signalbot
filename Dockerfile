FROM pblaas/signalcli:latest

LABEL MAINTAINER="patrick@kite4fun.nl"

USER root

RUN apt-get update && \
    apt-get -y install python3 python3-pip

COPY app.py botfunctions.py message.py requirements.txt ./app/
WORKDIR /app
RUN pip install -r requirements.txt

USER nobody

ENTRYPOINT ["python3", "app.py"]