FROM debian:bullseye-slim

LABEL MAINTAINER="patrick@kite4fun.nl"
ARG SIGNAL_CLI_VERSION='0.7.4'


## Install dependencies
RUN apt-get update && \
  mkdir /usr/share/man/man1 && \
  apt-get install -y apt-utils libterm-readline-perl-perl &&  \
  apt-get install -y openjdk-11-jre curl python3 python3-pip && \
  apt-get install -y locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8 

## Install Signal CLI
RUN curl -OL https://github.com/AsamK/signal-cli/releases/download/v$SIGNAL_CLI_VERSION/signal-cli-$SIGNAL_CLI_VERSION.tar.gz && \ 
  tar -zxvf signal-cli-$SIGNAL_CLI_VERSION.tar.gz && \
  rm -f signal-cli-$SIGNAL_CLI_VERSION.tar.gz && \
  ln -s signal-cli-$SIGNAL_CLI_VERSION signal 

## Install Python dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt

USER nobody
VOLUME /config
#ENTRYPOINT ["/signal/bin/signal-cli", "--config", "/config"]
CMD ["python3", "app.py"]