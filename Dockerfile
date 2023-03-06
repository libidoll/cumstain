FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-pyqt5 \
    libqt5gui5 \
    build-essential \
    ffmpeg \ 
    git && \
    pip3 install --upgrade pip && \
    mkdir /tmp/watermaker

WORKDIR /tmp
COPY . /tmp/

RUN pip3 install -r requirements.txt

CMD ["python3", "watermarker.py"]