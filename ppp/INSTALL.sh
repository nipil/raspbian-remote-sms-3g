#!/bin/sh

NAME=modem-3g
TARGET=/etc/ppp
SUBTARGET=peers

sudo rm -Rfv ${TARGET}/${NAME} && \
sudo cp -v -r ${NAME} ${TARGET} && \
sudo ln -v -f -s ${TARGET}/${NAME}/${NAME} ${TARGET}/${SUBTARGET}/
