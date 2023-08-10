# syntax=docker.io/docker/dockerfile:1.4

# build stage: includes resources necessary for installing dependencies
FROM --platform=linux/riscv64 cartesi/python:3.10-slim-jammy as build-stage

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential=12.9ubuntu3 \
    libopenblas0-serial libgomp1 libtiff5 libjpeg8 libopenjp2-7 zlib1g libfreetype6 liblcms2-2 libwebp7 libharfbuzz0b libfribidi0 libxcb1 libatomic1 \
    && rm -rf /var/lib/apt/lists/* \
    && find /var/log \( -name '*.log' -o -name '*.log.*' \) -exec truncate -s 0 {} \;

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY dapp/requirements.txt .

RUN pip install -r requirements.txt --no-cache \
    && find /opt/venv -type d -name __pycache__ -exec rm -r {} +

WORKDIR /opt/cartesi/dapp

COPY /dapp .
