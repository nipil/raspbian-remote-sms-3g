#!/bin/sh

sudo apt-get install python3-venv && \
python3 -m venv venv && \
venv/bin/pip3 install -r requirements.txt
