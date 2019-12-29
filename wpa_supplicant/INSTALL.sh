#!/bin/sh

NAME=wpa_supplicant.conf
TARGET=/etc/wpa_supplicant
PERMS=600

sudo cp -v ${NAME} ${TARGET}/${NAME} && \
sudo chmod -v ${PERMS} ${TARGET}/${NAME} && \
sudo systemctl restart wpa_supplicant.service
