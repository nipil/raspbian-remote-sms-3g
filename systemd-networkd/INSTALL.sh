#!/bin/sh

NAME='*.network'
TARGET=/etc/systemd/network

sudo cp -v -r ${NAME} ${TARGET}
