ARG PYTHON_VERSION=3.9.4-slim
FROM python:${PYTHON_VERSION}

LABEL maintainer="TQHOA <tqhoa8th@gmail.com>"

# set work directory
WORKDIR /zkit

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ="Asia/Ho_Chi_Minh"

COPY ./requirements.txt /zkit/requirements.txt

# install system dependencies
RUN apt-get update
#RUN apt-get install -y netcat
RUN apt-get -y install python3-pip
RUN pip install --upgrade pip

# Image modifications
RUN apt-get install -y libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libmagic1

RUN if [ ! -e /lib/libz.so ]; then \
    ln -s /usr/lib/x86_64-linux-gnu/libz.so /lib/ \
    ;fi

RUN if [ ! -e /lib/libjpeg.so ]; then \
    ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /lib/ \
    ;fi

# Install FFMPEG:
ARG INSTALL_FFMPEG=false
RUN echo "Oh dang look at that $INSTALL_FFMPEG"

RUN if [ ${INSTALL_FFMPEG} = true ]; then \
    apt-get install -y ffmpeg \
;fi
#RUN ffmpeg -version
#RUN ffmpeg -encoders
#RUN ffmpeg -decoders

RUN apt-get install curl -y

# install dependencies
#RUN pip install --no-cache-dir -r /zkit/requirements.txt
RUN pip3 install -r /zkit/requirements.txt

COPY ./src /zkit
