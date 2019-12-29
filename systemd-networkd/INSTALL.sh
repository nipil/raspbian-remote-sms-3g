#!/bin/sh

NAME='*.network'
TARGET=/etc/systemd/network

sudo systemctl enable systemd-networkd && \
sudo systemctl start systemd-networkd && \
sudo cp -v -r ${NAME} ${TARGET} && \
sudo systemctl restart systemd-networkd.service
